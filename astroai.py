import tkinter as tk
from tkinter import scrolledtext
import requests
from datetime import datetime

OPENAI_API_KEY = 'your-openai_API-key'

class GPTChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astro AI")
        
        self.root.geometry('600x600')
        
        self.root.configure(bg='#0d1440')
        
        self.title_label = tk.Label(root, text="Astro AI", font=("Gotham", 24), bg='#0d1440', fg='#ff69b4')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.create_input_field("Date of Birth (dd/mm/yyyy):", "dob", 1)
        self.create_input_field("Time of Birth (HH:MM):", "tob", 2)
        self.create_input_field("City of Birth:", "cob", 3)
        
        self.submit_button = tk.Button(root, text="Submit", font=("Gotham", 14), bg='#ff69b4', fg='white', command=self.submit_details)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.init_chat_interface()

        self.user_details = {}
        self.conversation_history = []

    def create_input_field(self, label_text, field_name, row):
        label = tk.Label(self.root, text=label_text, font=("Gotham", 12), bg='#0d1440', fg='white')
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(self.root, font=("Gotham", 12), bg='#333333', fg='white', width=40)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky='w')
        setattr(self, field_name, entry)

    def submit_details(self):
        self.user_details['dob'] = self.dob.get()
        self.user_details['tob'] = self.tob.get()
        self.user_details['cob'] = self.cob.get()
        self.user_details['tod'] = datetime.now().strftime("%d/%m/%Y")

        self.conversation_history = [
            {"role": "system", "content": self.construct_custom_prompt()}
        ]

        self.dob.delete(0, tk.END)
        self.tob.delete(0, tk.END)
        self.cob.delete(0, tk.END)

        self.clear_screen()
        self.display_message("System", "User details submitted successfully. Generating your personalized horoscope...", 'system')

        self.get_welcome_message()

        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.conversation_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.user_input.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.send_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.status_label.config(text="Ask me anything about astrology...")

    def construct_custom_prompt(self):
        return (
            f"You are an expert astrologist. You are chatting with a user who was born on {self.user_details['dob']} "
            f"at {self.user_details['tob']} in {self.user_details['cob']}. Today's date is {self.user_details['tod']}. "
            "Provide horoscopes and answer the user's questions in a friendly and informative manner."
        )

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def init_chat_interface(self):
        self.conversation_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Gotham", 12), bg='#0d1440', fg='white', height=20, width=60)
        self.conversation_area.configure(state='disabled')

        self.conversation_area.tag_configure('user_bold', font=("Gotham", 12, "bold"))
        self.conversation_area.tag_configure('bot_bold', font=("Gotham", 12, "bold"))
        self.conversation_area.tag_configure('user', background='#333333', foreground='#ffffff', justify='right')
        self.conversation_area.tag_configure('bot', background='#ff69b4', foreground='#ffffff', justify='left')
        self.conversation_area.tag_configure('system', background='#0d1440', foreground='#ff69b4', justify='center')
        
        self.user_input = tk.Entry(self.root, font=("Gotham", 12), bg='#333333', fg='white', width=40)
        self.send_button = tk.Button(self.root, text="Send", font=("Gotham", 14), bg='#ff69b4', fg='white', command=self.send_message)
        self.status_label = tk.Label(self.root, text="", font=("Gotham", 12), bg='#0d1440', fg='white')

    def get_welcome_message(self):
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {"role": "system", "content": "Generate a detailed horoscope and welcome message based on the user's birth details."},
                        {"role": "user", "content": f"User's date of birth is {self.user_details['dob']}, time of birth is {self.user_details['tob']}, and city of birth is {self.user_details['cob']}. Generate a welcome message in the following format: \nSun Sign: \n\nAs a , you are known for your . Today, the cosmos is encouraging you to embrace these traits fully.\nMoon in :\n\nWith the Moon in , your adventurous and optimistic side will shine. It's a great day to explore new ideas and broaden your horizons. Don't be afraid to step out of your comfort zone.\nPlanetary Influences:\n\nMercury in : Communication is key today. Engage in meaningful conversations and share your ideas. Your words have the power to inspire others.\nVenus in : Your charisma and charm are heightened. This is an excellent time for social interactions and expressing your creativity. You might find yourself the center of attention, and that's perfectly okay.\nDaily Tarot Card: The Star\n\nThe Star card represents hope, inspiration, and serenity. It suggests that you are on the right path and that your efforts will lead to positive outcomes. Trust in yourself and the universe.\nNumerology Insight:\n\nLife Path Number: 3\n\nAs someone with a Life Path Number of 3, creativity and self-expression are your strengths. Today, focus on activities that allow you to showcase your talents. Whether it's through art, writing, or any other creative outlet, let your imagination run wild.\nPersonal Day Number: 5\n\nThe energy of the number 5 is about change, adventure, and freedom. Be open to new experiences and embrace the unexpected. This is a day to be flexible and adaptable.\nToday's Affirmation:\n\n'I am open to new possibilities and trust that the universe is guiding me towards my highest good.'\nHealth Tip:\n\nEngage in a physical activity that excites you, like a dance class or a nature hike. Keeping your body active will help balance your mental and emotional energy.\nCareer and Finance:\n\nOpportunities for growth and advancement are on the horizon. Stay proactive and seize any chances to demonstrate your skills. Financially, be mindful of impulsive spending. Plan and budget wisely.\nLove and Relationships:\n\nYour social charm is at its peak. This is a great day to connect with loved ones and strengthen your relationships. Single Aquarians might find new romantic prospects through social gatherings or online interactions.\nSpiritual Guidance:\n\nTake a few moments for mindfulness or meditation. Connecting with your inner self will bring clarity and peace. Consider journaling your thoughts and feelings to gain deeper insights.\nLucky Colors:\n\nShades of blue and turquoise will enhance your intuitive abilities and bring a sense of calm and balance.\nLucky Numbers:\n\n3, 5, 9, 12, 21"}
                    ],
                    'max_tokens': 500,
                    'temperature': 0.7
                }
            )
            response_data = response.json()
            print(response_data)
            if 'choices' in response_data and len(response_data['choices']) > 0:
                welcome_message = response_data['choices'][0]['message']['content'].strip()
                self.display_message("AstroAI", welcome_message, 'bot')
            else:
                self.display_message("Error", "Invalid response from OpenAI", 'bot')
        except Exception as e:
            self.display_message("Error", str(e), 'bot')

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You", user_message, 'user')
            self.user_input.delete(0, tk.END)
            self.conversation_history.append({"role": "user", "content": user_message})
            self.get_response_from_gpt3()

    def display_message(self, sender, message, tag):
        self.conversation_area.configure(state='normal')
        self.conversation_area.insert(tk.END, f"{sender}: ", f"{tag}_bold")
        self.conversation_area.insert(tk.END, f"{message}\n", tag)
        self.conversation_area.configure(state='disabled')
        self.conversation_area.yview(tk.END)

    def get_response_from_gpt3(self):
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': self.conversation_history,
                    'max_tokens': 150,
                    'temperature': 0.7
                }
            )
            response_data = response.json()
            print(response_data)
            if 'choices' in response_data and len(response_data['choices']) > 0:
                gpt_response = response_data['choices'][0]['message']['content'].strip()
                self.conversation_history.append({"role": "assistant", "content": gpt_response})
                self.display_message("AstroAI", gpt_response, 'bot')
            else:
                self.display_message("Error", "Invalid response from OpenAI", 'bot')
        except Exception as e:
            self.display_message("Error", str(e), 'bot')

if __name__ == "__main__":
    root = tk.Tk()
    app = GPTChatbotApp(root)
    root.mainloop()