import pytest
from ssh_log import SSHLogEntry, SSHLogEntryPasswordRejected, SSHLogEntryPasswordAccepted, SSHLogEntryError, SSHLogEntryOther
from ssh_log_journal import SSHLogJournal
from ipaddress import AddressValueError

def test_extract_timestamp():
    log_entry = SSHLogEntry.create_specific_log("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2")
    assert log_entry.timestamp.strftime("%Y-%m-%d %H:%M:%S") == "2024-12-10 06:55:48"

def test_extract_ipv4_valid():
    log_entry = SSHLogEntry.create_specific_log("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2")
    assert str(log_entry.ipv4) == "173.234.31.186"

def test_extract_ipv4_invalid():
    with pytest.raises(AddressValueError):
        SSHLogEntry.create_specific_log("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 666.777.88.213 port 38926 ssh2")

def test_extract_ipv4_none():
    log_entry = SSHLogEntry.create_specific_log("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster port 38926 ssh2")
    assert log_entry.ipv4 is None

@pytest.mark.parametrize("class_entry, log", [
    (SSHLogEntryPasswordRejected, "Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster port 38926 ssh2"),
    (SSHLogEntryPasswordAccepted, "Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2"),
    (SSHLogEntryError, 'Dec 10 11:03:40 LabSZ sshd[25448]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]'),
    (SSHLogEntryOther, 'Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!')
])
def test_append(class_entry, log):
    journal = SSHLogJournal()
    journal.append(log)
    print(journal[-1][0].__class__)
    assert isinstance(journal[0][0], class_entry)