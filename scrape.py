
import difflib
import sys
import os
import yaml
from collections import defaultdict
import re
import logging

log = logging.getLogger('scrape')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

class Reason(object):
    def get_description(self):
        return self.description

class GenericReason(Reason):
    """
    A reason inferred from summary->failure_reason string
    """
    def __init__(self, failure_reason, description=None):
        self.failure_reason = failure_reason
        if description is None:
            self.description = failure_reason
        else:
            self.description = description

    def match(self, job):
        ratio = difflib.SequenceMatcher(None, self.failure_reason, job.get_failure_reason()).ratio()
        #log.debug("GenericReason.match: {0}\n {1}\n {2}".format(ratio, self.failure_reason, job.get_failure_reason()))
        return ratio > 0.5

class RegexReason(Reason):
    """
    A known reason matching a particular regex to failure reason
    """
    def __init__(self, regexes, description):
        self.description = description
        if not isinstance(regexes, list):
            self.regexes = [regexes]
        else:
            self.regexes = regexes

    def match(self, job):
        for regex in self.regexes:
            if re.match(regex, job.get_failure_reason()) is not None:
                return True

        return False

class Job(object):
    def __init__(self, path, job_id):
        self.path = path
        self.job_id = job_id

        summary_path = os.path.join(self.path, "summary.yaml")
        self.summary_data = yaml.load(open(summary_path, 'r'))

    def get_success(self):
        return self.summary_data['success']

    def get_failure_reason(self):
        return self.summary_data['failure_reason']

def give_me_a_reason(job):
    """
    If no existing reasons match the job, generate the most specific reason we can
    """

    known_reasons = [
        # If the failure reason indicates no packages found...
        RegexReason([
            "Failed to fetch package version from http://",
            "Command failed on .* with status 100: 'sudo apt-get update"]
            , "Missing packages"),
        # If there is a valgrind complaint and it's for X service type...
        RegexReason("saw valgrind issues", "Valgrind"),
        # If a timeout was hit
        RegexReason("with status 124", "Timeout"),
    ]

    # If there is a stacktrace and it contains lockdep...
    # If there is a segfault and no stacktrace exists...

    for r in known_reasons:
        if r.match(job):
            return r

    return GenericReason(job.get_failure_reason())


class Scraper(object):
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def analyze(self):
        entries = os.listdir(self.target_dir)
        jobs = []
        for entry in entries:
            job_dir = os.path.join(self.target_dir, entry)
            if os.path.isdir(job_dir):
                jobs.append(Job(job_dir, entry))

        log.info("Found {0} jobs".format(len(jobs)))

        passes = []
        reasons = defaultdict(list)

        for job in jobs:
            if job.get_success():
                passes.append(job)
                continue

            matched = False
            for reason, reason_jobs in reasons.items():
                if reason.match(job):
                    reason_jobs.append(job)
                    matched = True
                    break

            if not matched:
                reasons[give_me_a_reason(job)].append(job)

        log.info("Found {0} distinct failure reasons".format(len(reasons)))
        for reason, jobs in reasons.items():
            job_spec = [j.job_id for j in jobs].__str__() if len(jobs) < 10 else "{0} jobs".format(len(jobs))
            log.info(reason.get_description())
            log.info(job_spec)
            log.info("")

if __name__ == '__main__':
    Scraper(sys.argv[1]).analyze()
