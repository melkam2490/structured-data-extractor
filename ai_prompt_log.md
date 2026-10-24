# AI Prompt and Code Audit Log

## 1. Original Prompt

I asked AI to help build a Python invoice extraction system using Pydantic v2. The system should extract invoice information, validate the data, repair errors, and send failed records to a dead-letter queue.

## 2. Initial AI-Generated Code

The first version included:

- A Pydantic invoice schema
- A function to validate invoice data
- A Streamlit user interface
- A basic retry and fallback function

## 3. Issues Found During Review

### Issue 1: Missing Import

The fallback code used `os.makedirs()` without importing `os`.

**Fix:** Added `import os` so the program can create the dead-letter queue folder.

### Issue 2: Validation Errors Were Not Sent Back to AI

The first retry function did not send the previous validation error back to the AI. This meant the AI did not have enough information to correct its previous extraction.

**Fix:** Updated the retry function to send the previous error to the AI and ask it to correct the invoice data before trying again.

### Issue 3: Test Folder Was Missing

Pytest could not find the tests because the test folder had not been created.

**Fix:** Created a `tests` folder and added test files for schema validation, fallback behavior, and invoice text ingestion.

## 4. Current Test Results

**Result: 9 tests passed.**

The tests cover:

- Valid invoice data
- Positive quantity requirement
- Supported currency requirement
- Invoice total reconciliation
- Negative tax rejection
- Successful reflection and retry on the second attempt
- Failed extraction being sent to the dead-letter queue
- HTML invoice text extraction
- PDF file ingestion

## 5. Remaining Improvements

- Improve the PDF test to verify extracted text, not just that a PDF can be opened.
- Improve error handling and JSON repair.
- Improve the user interface and documentation.
- Test the application with more invoice examples, including missing or incorrect information.

## 6. Summary

AI helped create the initial code, but I reviewed and tested the implementation. I fixed the missing import, improved the reflection and retry process, and added tests for validation, ingestion, and failure handling. The current test suite passes all nine tests.
