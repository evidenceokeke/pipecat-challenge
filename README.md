# Pipecat Phone Chatbot - Silence Detection and Post-Call Summary

This project extends the Pipecat Phone Chatbot example (https://github.com/pipecat-ai/pipecat/tree/main/examples/phone-chatbot) by adding the following functionalities:

* **Silence Detection**: Detects 10+ seconds of silence and plays a TTS prompt to check if the caller is still present. After three unanswered prompts, the call is gracefully terminated.
  ![image](https://github.com/user-attachments/assets/12d0924f-d2cc-4d6a-8aab-c3512e085e8b)

  
* **Post-Call Summary**: Logs call duration, silence events, and other call statistics to a call_summary.log file for post-call analysis.
  ![image](https://github.com/user-attachments/assets/f1077d4e-3d66-404e-bae0-140f218d8acc)





**SETUP AND INSTALLATION**

1. Fork the repository
2. Clone the repository:
   ```
   git clone <your-fork-url>
   cd phone-chatbot
   ```
3. Create an activate a virtual environment
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   ***NOTE*** - If you are using Windows, you may encounter issues with ```daily-python``` as some of its dependencies are not compatible with Windows. Use WSL (Ubuntu) terminal instead and install Python 3.10 for compatibility.

5. Copy the example environment file:
   ```
   cp env.example .env
   ```

   Edit .env to include API keys for Daily, Deepgram, Cartesian, and OpenAI/Google API.

6. Install Ngrok and start it on:
   ```
   ngrok http 7860

   ```

   or with your custom domain if you are using the paid version. You can also run it locally as well.

 


**RUNNING THE APPLICATION**
1. Start the bot runner service:
   ```
   python bot_runner.py --host localhost
   ```
2. You can initiate a call using curl or postman:
   ```
   curl -X POST "http://localhost:7860/start" \
   -H "Content-Type: application/json" \
   -d '{
      "config": {
        "simple_dialin": {
          "testInPrebuilt": true
        }
      }
   }'
   ```
    <img width="357" alt="image" src="https://github.com/user-attachments/assets/37453b29-17c2-4f58-96f4-50eca74ccc4b" />


3. Click on the Daily room link providec in the response. It may take a moment for the bot to join. To trigger silent detection prompt, remain silent for 10 seconds or longer.

 ![image](https://github.com/user-attachments/assets/1fc7fe54-d5cf-4f68-9c00-821d540fda78)

 ![image](https://github.com/user-attachments/assets/603ef7db-d7e8-4db8-845b-571b4defb869)




**IMPLEMENTATION DETAILS**

1. Silent detection implemented on ```simple_dialin.py``` using Pipecat's ```UserIdleProcessor```
2. Post-Call summary implemented on ```simple_dialin.py``` using Loguru's ```loggers```. It begins when the first participant joins the call.

**RESOURCES**
1. Detecting Idle Users: https://docs.pipecat.ai/guides/fundamentals/detecting-user-idle
2. python loguru output to stderr and a file: http://stackoverflow.com/questions/76575878/python-loguru-output-to-stderr-and-a-file
3. Help install daily python 3.12 #290: https://github.com/pipecat-ai/pipecat/issues/290

   
