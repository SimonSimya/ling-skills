# Regression fixtures for safety-check.py

Every line below is a case the scanner got WRONG at some point. All values are
fabricated. `MUST-LEAK` lines must exit 2, `MUST-WARN` lines must produce a `read` line
without failing, and `MUST-PASS` lines must not fire the credential rule. Run `python3 tests/run.py`.

## MUST-LEAK
DB_PASSWORD=hunter2supersecret
SLACK_BOT_TOKEN=xoxb-9999999999-abcdefghij
OPENAI_API_KEY=sk-proj-AAAAbbbbCCCCddddEEEEffffGGGG
MY_TOKEN = "abcdefghijklmnop"
key = sk-projAAAAbbbbCCCCddddEEEEffffGG
app_token = xapp-1-A012345678-9876543210-abcdef
hook = https://hooks.slack.com/services/T01ABCDEFG/B02HIJKLMN/ZzYyXxWwVvUu
google_secret = GOCSPX-aBcDeFgHiJkLmNoPqRs
dsn = https://abc123@o12345.ingest.sentry.io/456789
test_key = sk_test_51H8xQ2KaBcDeFgHiJkLmNo
live = sk_live_51H8xQ2KaBcDeFgHiJkLmNo
sheet = "1mS6DSxrjGGk4OY8_IapuDL64wcWZkLioyShRtg8Pq-Q"
board = https://app.clickup.com/9013/v/li/901300123456
drive = https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQrStUvWxYz012345/view
project_id = ling-production-1234
//registry.npmjs.org/:_auth=YWRtaW46U3Vyc2VjcmV0MTIz

## MUST-WARN
> These must surface for a human to read, but must not fail the build: only a
> person can tell a worked example from a leak.

colleague = "haseeb@ling-app.com"
user wrote in from angry.customer@gmail.com
We hit $8M ARR this year.
Salary bands are in the attached sheet.
CONFIDENTIAL - internal only

## MUST-PASS
api_key = os.environ["OPENAI_API_KEY"]
token = os.getenv("SLACK_TOKEN")
password = config.get("db_password")
secret = process.env.STRIPE_SECRET
key = ${MY_API_KEY}
Contact support@ling-app.com with questions.
Read the sheet id from config; ask the user for it.
password = "correct-horse-battery-staple"
token: replace-with-your-own-token
api_key = "<YOUR_API_KEY_HERE>"
sha256 = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
