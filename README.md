# Gmail TLDR Newsletter Text-to-Speech (TTS)

## How it works
The program will get the TLDR Newsletter that was sent today, parse the content of that email, and output the title and summary of the articles mentioned in the email to an output txt file. The content of the txt file will be converted to an audio file via Google's Text-to-Speech API. This audio file will then be sent to your email where you can download and listen to the audio.


## Technologies Used
* Python
* Gmail API
* Cloud Text-to-Speech API
* Beautiful Soup 4


## Instructions
1. Create a Google CLoud Project (https://developers.google.com/workspace/guides/create-project)
2. Enable "Gmail API" and "Cloud Text-to-Speech API". Note: You may need to enable billing before you can start using Google APIs. (https://support.google.com/googleapi/answer/6158841?hl=en)
3. Create OAuth 2.0 Client ID - download the JSON file, insert the file into your project directory, and rename it to "credentials.json" (https://developers.google.com/workspace/guides/create-credentials#oauth-client-id)
4. Create Service Account - download the JSON file, insert the file into your project directory, and rename it to "tts_key.json" (https://developers.google.com/workspace/guides/create-credentials#service-account)
5. Grant user access to project - use your email (https://cloud.google.com/iam/docs/granting-changing-revoking-access)
6. Replace the variable "tldrEmail" to the actual TLDR Newsletter Email in file parseEmail.py
7. Assign "message['to']" and "message['from']" to the email you want the audio file to be sent to, in file sendAudio.py
8. Open a terminal and navigate to project directory
9. run "python parseEmail.py"
10. log in with your gmail
11. click "continue" to gain access to the app
12. Check/enable "View your email messages and settings.", "Send email on your behalf.", and "Manage drafts and send emails.", then click "continue" to complete authentication. This will generate the file "token.json" in your project directory.
13. run "python parseEmail.py"
14. run "python textSynthesize.py"
15. run "python sendAudio.py"
