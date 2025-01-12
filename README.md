

<a href="https://github.com/SuwanSankaja/Private_Files/blob/main/Medical_Chatbot/DSE%20Group%20Project%20%20%20Group%2022_1080p.mp4">
    <img src="https://github.com/SuwanSankaja/Private_Files/blob/main/Medical_Chatbot/Homepage.png" alt="Watch the video" width="600" height="300">
</a>



# 🤖 Medical Chatbot


Welcome to the **Medical Chatbot**, an intelligent and user-friendly virtual assistant designed to provide healthcare guidance. Built on the Rasa framework, this chatbot can handle queries about hospitals, doctors, first aid, and more with natural language understanding.

## 🚀 Features

- 🏥 **Healthcare Assistance**: Instantly get details about clinics, doctors, and hospital services.
- 📅 **Appointment Booking**: Effortlessly schedule medical appointments with specialists.
- 🩹 **First Aid Guidance**: Quick assistance for emergencies like burns, fractures, and more.
- 🤝 **Natural Conversations**: Seamless and intuitive dialogue flow.
- ⚙️ **Custom Integrations**: API and database-enabled responses for dynamic data.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medical-chatbot.git
   cd medical-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install rasa
   pip install -r requirements.txt
   ```

3. Train the model:
   ```bash
   rasa train
   ```

4. Run the chatbot:
   ```bash
   rasa run
   rasa run actions
   ```

5. Test the chatbot locally:
   ```bash
   rasa shell
   ```

## 🗂️ Project Structure

```plaintext
📁 data/         # Training data for intents, entities, and stories
📁 actions/      # Custom action scripts
📁 models/       # Trained Rasa models
📝 domain.yml    # Defines intents, slots, responses, and actions
📝 config.yml    # Pipeline and policies configuration
📝 endpoints.yml # External services and action endpoints
```

## 🌟 Key Functionalities

### Intents

- 💬 **General Queries**: Greet, goodbye, and bot-related queries.
- 🩺 **Medical Assistance**: Support for burns, fractures, and other emergencies.
- 🏥 **Hospital Information**: Parking, cafeteria, contact details, and services.
- 📅 **Appointment Management**: Booking, rescheduling, and doctor availability.

### Custom Actions

- Fetch real-time details about hospital services.
- Handle dynamic appointment scheduling.

## 💡 Usage Examples

### Sample User Queries

- 🤔 "Tell me about the hospital's parking facilities."
- 📅 "How can I book an appointment with Dr. Smith?"
- 🩹 "What should I do for a minor burn?"
- ☕ "Is there a cafeteria in the hospital?"

### Responses

The chatbot intelligently detects user intents and fills slots to provide tailored, context-aware replies.

## 🖼️ Screenshots

![Chat Interface](https://github.com/SuwanSankaja/Private_Files/blob/main/Medical_Chatbot/chatbot_UI.png)

## 👥 Contribution Guidelines

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request.


