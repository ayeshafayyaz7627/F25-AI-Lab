"""Creates corpus.json and queries.json (synthetic teaching data, not real policies)."""
import json
from pathlib import Path

docs = {
"late": (
"Assessment Policy Handbook, Section 4. All coursework must be submitted before the stated deadline through the official channel. "
"Late submission is normally penalized by ten percent of the total mark for each day after the deadline, and work submitted more than five days late is not accepted. "
"Students should plan their time carefully and begin assignments early so that technical problems do not cause delays. "
"Illness extensions require medical evidence before the deadline. "
"The evidence must be a certificate issued by a registered doctor and must state the dates on which the student was unable to work. "
"Requests made after the deadline are considered only in exceptional circumstances and must be approved by the programme coordinator. "
"Group projects follow the same rules, but each member must submit a separate request for an extension. "
"Students who experience repeated difficulties are encouraged to contact the student advisor, who can explain the support services available on campus, including counselling, study skills workshops and peer tutoring sessions. "
"Marks for late work are published together with the rest of the class results, and penalties cannot be appealed unless an administrative error is found."),
"late_lab": (
"Laboratory Handbook, Report Deadlines. Laboratory reports are submitted one week after each practical session unless the instructor announces a different date. "
"Late lab reports lose five percent of the mark per day, and reports more than three days late receive zero. "
"Lab illness extensions need a note from the department office within two days of the deadline. "
"This rule is different from the general coursework policy because laboratory equipment bookings cannot be repeated at short notice. "
"Students who miss a practical session because of illness must contact the lab coordinator on the same day to arrange a catch-up slot, and the slot is offered only once per semester. "
"Reports must include the raw data sheet signed by the demonstrator, a short method section and a discussion of sources of error. "
"Reports that contain copied text are referred to the academic integrity panel. "
"Group practicals are marked individually when each student keeps a separate lab book, and groups of more than three students are not permitted. "
"Safety rules must be confirmed in writing before the first session begins."),
"password": (
"IT Help Desk Guide, Accounts. Every student receives a university account when enrolment is confirmed. "
"Accounts give access to email, the learning portal, library databases and campus wireless networks. "
"Reset a forgotten password using the recovery link. "
"The link is sent to the personal email address stored in the student record and stays valid for thirty minutes, after which a new link must be requested from the login page. "
"Never share recovery codes with other people, including friends, classmates or staff members who claim to work for the help desk. "
"The real help desk will never ask for a password by telephone or email. "
"If the personal email address is out of date, students must visit the help desk in person with their student card so that the record can be corrected. "
"After three failed login attempts the account is locked for fifteen minutes to protect it from unauthorised access. "
"Staff accounts follow a different procedure and are managed by the central IT office. "
"Students are advised to choose passwords of at least twelve characters and to avoid reusing passwords from other websites."),
"assignment": (
"Learning Portal Guide, Submissions. The learning portal is the only approved system for handing in coursework, and email submissions are not accepted unless the instructor gives written permission. "
"Upload assignments through the learning portal. "
"Open the course page, select the assignment title, attach the file and press the submit button, then keep the confirmation receipt until final marks are released. "
"Submit the final file as a PDF so that formatting remains unchanged on every device. "
"Source code may be submitted as a single zip archive, provided that it does not contain virtual environments, model files or any private credentials. "
"Each file must be smaller than fifty megabytes, and the portal rejects files with unusual extensions. "
"Students can replace a submission as many times as they like before the deadline, and only the latest version is marked. "
"If the portal is unavailable close to a deadline, take a screenshot of the error message and contact the course instructor immediately so that the problem can be recorded and a fair decision can be made about the submission time."),
"contractor": (
"Workplace Policy Notes, Remote Work. Employees may request remote work with manager approval, and the arrangement is reviewed every six months by the department head. "
"The standard arrangement allows up to two remote days per week, although teams with client meetings may agree different patterns. "
"Contractors can work remotely only if the signed contract permits it. "
"Employee rules do not apply to contractors, because contractors are engaged under separate agreements that define their working location, hours and equipment. "
"A contractor who wishes to change the working location must ask the contract owner for a written amendment before starting remote work. "
"Remote workers must use the company virtual private network, keep their devices updated and avoid working from public places when handling confidential material. "
"Equipment allowances are paid to employees only after probation has been completed, and they cannot be claimed retrospectively. "
"Managers must record every remote arrangement in the human resources system so that safety and insurance responsibilities remain clear. "
"Questions about unusual cases should be sent to the policy owner in the human resources office."),
"printer": (
"Equipment Troubleshooting Sheet, Office Printers. This sheet covers common faults on the shared office printers and should be read before a technician is called. "
"For blank printer pages, check ink levels and run the cleaning utility. "
"Print a test page afterwards to confirm that the fault has been fixed. "
"If the page is still blank, switch the printer off for one minute, reinstall the cartridge and repeat the cleaning utility once more. "
"Warning: never open the rear panel while the printer is powered on, because the heating unit stays hot for several minutes after use. "
"Paper jams should be cleared by pulling the sheet gently in the direction of travel, and torn fragments must be removed completely before printing again. "
"Scanners are a separate device and use different steps; for a blank scanner image, check document placement and select the correct scanning source. "
"Network printing problems should be reported to the IT help desk together with the printer name and the exact message shown on the display. "
"Toner and ink orders are placed monthly, and urgent requests need approval from the office manager."),
}

evidence = {
"late": "Illness extensions require medical evidence before the deadline.",
"password": "Reset a forgotten password using the recovery link.",
"assignment": "Upload assignments through the learning portal.",
"contractor": "Contractors can work remotely only if the signed contract permits it.",
"printer": "For blank printer pages, check ink levels and run the cleaning utility.",
}

questions = [
("What is required for illness extensions?", "late", "dev"),
("How do I reset a forgotten password?", "password", "dev"),
("Where do I upload assignments?", "assignment", "dev"),
("Can contractors work remotely?", "contractor", "dev"),
("What do I do for blank printer pages?", "printer", "test"),
("How can I recover my login access?", "password", "test"),
("How should I hand in my coursework?", "assignment", "test"),
("What proof is needed when I was ill?", "late", "test"),
("What are tomorrow's flight prices?", None, "test"),
("Who won the football match?", None, "test")]

queries = [dict(query=q, doc=d, evidence=evidence[d] if d else None, split=s)
           for q, d, s in questions]

for name, data in [("corpus.json", docs), ("queries.json", queries)]:
    if Path(name).exists():
        raise FileExistsError("Refusing to overwrite " + name)
    Path(name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Created corpus.json and queries.json")
for k, v in docs.items():
    print(k, len(v.split()), "words")
