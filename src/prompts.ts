// prompts.ts - as is from CodeRabbits repo

import { type Inputs } from './inputs';


export class Prompts {
  summarize: string;
  summarizeReleaseNotes: string;

  
  summarizeFileDiff = `## GitHub PR Title

\`$title\` 

## Description

\`\`\`
$description
\`\`\`

## Diff

\`\`\`diff
$file_diff
\`\`\`

## Instructions

I would like you to succinctly summarize the diff within 100 words.
If applicable, your summary should include a note about alterations 
to the signatures of exported functions, global data structures and 
variables, and any changes that might affect the external interface or 
behavior of the code.
`;

  triageFileDiff = `Below the summary, I would also like you to triage the diff as \`NEEDS_REVIEW\` or 
\`APPROVED\` based on the following criteria:

- If the diff involves any modifications to the logic or functionality, even if they 
  seem minor, triage it as \`NEEDS_REVIEW\`. This includes changes to control structures, 
  function calls, or variable assignments that might impact the behavior of the code.
- If the diff only contains very minor changes that don't affect the code logic, such as 
  fixing typos, formatting, or renaming variables for clarity, triage it as \`APPROVED\`.

Please evaluate the diff thoroughly and take into account factors such as the number of 
lines changed, the potential impact on the overall system, and the likelihood of 
introducing new bugs or security vulnerabilities. 
When in doubt, always err on the side of caution and triage the diff as \`NEEDS_REVIEW\`.

You must strictly follow the format below for triaging the diff:
[TRIAGE]: <NEEDS_REVIEW or APPROVED>
`;

  summarizeChangesets = `Provided below are changesets in this pull request. Changesets 
are in chronological order and new changesets are appended to the
end of the list. The format consists of filename(s) and the summary 
of changes for those files. There is a separator between each changeset.
Your task is to deduplicate and group together files with
related/similar changes into a single changeset. Respond with the updated 
changesets using the same format as the input. 

$raw_summary
`;

  summarizePrefix = `Here is the summary of changes you have generated for files:
      \`\`\`
      $raw_summary
      \`\`\`
`;

  summarizeShort = `Your task is to provide a concise summary of the changes. This 
summary will be used as a prompt while reviewing each file and must be very clear for 
the AI bot to understand. 

Instructions:

- Focus on summarizing only the changes in the PR and stick to the facts.
- Do not provide any instructions to the bot on how to perform the review.
- Do not mention that files need a thorough review or caution about potential issues.
- Do not mention that these changes affect the logic or functionality of the code.
- The summary should not exceed 500 words.
`;

  reviewFileDiff = `## GitHub PR Title

\`$title\` 

## Description

\`\`\`
$description
\`\`\`

## Summary of changes

\`\`\`
$short_summary
\`\`\`

## IMPORTANT Instructions

Input: New hunks annotated with line numbers and old hunks (replaced code). Hunks represent incomplete code fragments.
Additional Context: PR title, description, summaries and comment chains.
Task: Review new hunks for substantive issues using provided context and respond with comments if necessary.
Output: Review comments in markdown with exact line number ranges in new hunks. Start and end line numbers must be within the same hunk. For single-line comments, start=end line number. Must use example response format below.
Do NOT recommend indentation fixes as you will receive change hunks (only those lines that have been changed), use the context surrounding the change hunk to point out any issues that need commenting
Use fenced code blocks using the relevant language identifier where applicable.
Don't annotate code snippets with line numbers. Format and indent code correctly.
Do not use suggestion code blocks.

For fixes, use diff code blocks, marking changes with "+" or "-". The line number range for comments with fix snippets must exactly match the range to replace in the new hunk.

- Do NOT provide general feedback, summaries, explanations of changes, indentation inconsistency erroes, or praises 
  for making good additions. 
- Focus solely on offering specific, objective insights based on the 
  given context and refrain from making broad comments about potential impacts on 
  the system or question intentions behind the changes or indentation problems.

If there are no issues found on a line range, you MUST respond with the 
text "LGTM!" for that line range in the review section. 

## Changes made to 'filename' for your review

{lines}

### Example response

Lines 22-22:
There's a syntax error in the add function.
\`\`\`diff
-    retrn z
+    return z
\`\`\`
---
Lines 24-25:
LGTM!
---

`;


  rayyanPrompt = `I have a git diff file containing before and after changes (from a pull request). I need a comprehensive code review in markdown format based on the following criteria:

1. **Overview of Changes**: Summarize the purpose of the changes and what has been added, removed, or modified.
2. **Code Quality and Best Practices**: Assess code readability, structure, and whether it adheres to best practices and coding standards. Identify any areas for refactoring or improvement.
3. **Performance Considerations**: Comment on the performance impact of the changes, including memory usage, computational efficiency, and any opportunities for optimizations.
4. **Testing and Validation**: Analyze the test coverage, ensuring the changes are properly validated. Mention any missing tests or untested edge cases.
5. **Security Implications**: Highlight any potential security issues, such as improper input validation or insecure data handling, and suggest ways to address them.
6. **Documentation and Comments**: Review the quality of the documentation and inline comments. If there are none, then try and recommend some fitting comments for specific snippets of inline code. Ensure the changes are properly explained for future maintainers.
7. **Impact Analysis**: Assess how the changes affect other parts of the codebase or system. Identify any potential side effects or integration issues.
8. **Potential Risks and Red Flags**: Identify any risks that could arise from the changes, such as regressions or unstable behavior.
9. **Future Considerations**: Suggest areas where the code could be further improved or refactored in future iterations.

Here is the contents of the diff file: $file_diff

**IMPORTANT**
- You need to reference every point you make with a snippet from inside the code!
- If there are changes for multiple files in the diff, treat them as separate code reviews but under the same section heading!

---

# SparkleBot Code Review Report 

## **Overview of Changes**  
The changes introduce token-based user authentication, replacing the previous session-based approach. This includes new functions for generating and validating tokens, as well as modifications to session management logic. Deprecated functions and unused imports have been removed.
python
# Before: Session-based user authentication
def login_user(session):
    # authenticate user and start session
    pass

# After: Token-based user authentication
def login_user(token):
    # authenticate user and return token
    pass


## **Code Quality and Best Practices**  
- The code is generally well-written, but some areas need improvement. For instance, in <auth_handler.py>, there's duplicated code for token generation that could be refactored into a reusable function.
python
# Current code - duplication of token generation logic
def generate_access_token():
    token = create_token()
    return token

def generate_refresh_token():
    token = create_token()
    return token

# Suggested refactor
def generate_token(token_type):
    token = create_token()
    return token


- The function <validate_credentials()> can be renamed to something more descriptive, such as <authenticate_user()>, for better clarity.

# Before
def validate_credentials():
    # validation logic
    pass

# After (recommended)
def authenticate_user():
    # validation logic
    pass


- Use of consistent error handling could be improved, especially in cases where exceptions are raised but not properly caught.


## **Performance Considerations**  
- The transition to token-based authentication should improve scalability in the long run. However, handling user data in memory for validation might slow down performance if the database grows. Introducing lazy loading or batched processing could mitigate this issue.
# Current implementation
users = db.get_all_users()
for user in users:
    process_user(user)

# Suggested improvement using pagination
def get_users(page_size):
    for page in range(0, db.total_users(), page_size):
        users = db.get_users(page, page_size)
        for user in users:
            process_user(user)
  

## **Testing and Validation**  
- While the basic functionality has been tested, theres a lack of coverage for edge cases, such as expired tokens or malformed tokens. Additional test cases could ensure the robustness of the authentication process.
- Input validation tests for security concerns (e.g., SQL injection, XSS) are missing and should be included.

# Suggested edge case tests
def test_expired_token():
    token = generate_token(expired=True)
    assert not validate_token(token)

def test_malformed_token():
    token = "malformed_token_string"
    assert not validate_token(token)



## **Security Implications**  
- The token-based approach improves security by minimizing session persistence, but care should be taken to store tokens securely and prevent token tampering.
- Ensure that user inputs in <validate_token()> are strictly validated to avoid potential injection attacks.
# Current validation method
def validate_token(token):
    if token in valid_tokens:
        return True
    return False

# Improved validation to prevent injection attacks
def validate_token(token):
    if not isinstance(token, str) or len(token) != expected_length:
        return False
    if token in valid_tokens:
        return True
    return False



## **Documentation and Comments**  
- The comments provided are minimal and could be more descriptive, especially around critical functions like <generate_token()>.
- While the overall code logic is relatively straightforward, future developers may benefit from more detailed inline comments explaining why certain decisions were made, particularly around security.

# Current comment
def generate_token():
    pass  # generates token

# Suggested improvement with detailed explanation
def generate_token():
    #Generates a new authentication token for the user.
    #This token is used to authenticate the user on subsequent requests
    #and should be stored securely.

    pass



## **Impact Analysis**  
- The introduction of token-based authentication affects user login, session management, and access control across the system. Any existing user session logic will need to be fully migrated to tokens, and any part of the system interacting with sessions may need updates.
- Ensure the change doesn't break any external services or APIs relying on the previous session-based method.
# Changes affecting session management
# Before
def manage_session(session):
    pass  # session management logic

# After
def manage_token(token):
    pass  # token management logic



## **Potential Risks and Red Flags**  
- The risk of introducing token management without robust validation could expose the system to security risks like token forgery or replay attacks. Ensure proper token invalidation and refresh mechanisms are in place.
- If any part of the system still relies on session-based authentication, it might cause conflicts until fully migrated.


# Missing token invalidation mechanism
def invalidate_token(token):
    valid_tokens.remove(token)



## **Future Considerations**  
- The current token generation method works well for small-scale applications, but for larger systems, consider using more sophisticated token handling (e.g., JWT with refresh tokens) for scalability and security.
- In the future, you might also consider adding multi-factor authentication (MFA) to enhance security further.
- Refactoring could be done in the future to consolidate duplicated logic for token creation and validation into a single module.

### Suggested MFA logic for future implementation
def send_otp(user):
    otp = generate_otp()
    send_to_user(user, otp)


---

Please use the example report as a reference to generate a similarly detailed code review based on the before and after code changes provided.

`;

  constructor(summarize = '', summarizeReleaseNotes = '') {
    this.summarize = summarize;
    this.summarizeReleaseNotes = summarizeReleaseNotes;
  }

  renderSummarizeFileDiff(inputs: Inputs, reviewSimpleChanges: boolean): string {
    //let prompt = this.summarizeFileDiff;
    let prompt = this.rayyanPrompt;
    if (!reviewSimpleChanges) {
      prompt += this.triageFileDiff;
    }
    return inputs.render(prompt);
  }

  renderSummarizeChangesets(inputs: Inputs): string {
    return inputs.render(this.summarizeChangesets);
  }

  renderSummarizeShort(inputs: Inputs): string {
    const prompt = this.summarizePrefix + this.summarizeShort;
    return inputs.render(prompt);
  }

  renderReviewFileDiff(inputs: Inputs): string {
    return inputs.render(this.reviewFileDiff);
  }
}
