# লাইভ এক্সচেঞ্জ রেট API থেকে ডেটা আনতে requests মডিউল ইম্পোর্ট করছি
import requests

# কারেন্সি কনভার্টার ক্লাস তৈরি
class CurrencyConverter:
    # কনস্ট্রাক্টর ফাংশন — ইনপুট নেবে: অ্যামাউন্ট, সোর্স কারেন্সি, টার্গেট কারেন্সি, আর লগারের অবজেক্ট
    def __init__(self, amount, from_currency, to_currency, logger):
        self.amount = amount
        self.from_currency = from_currency.upper()  
        self.to_currency = to_currency.upper()
        self.logger = logger  # লগিং ব্যবস্থার জন্য Logger অবজেক্ট

    # রিয়েল টাইমে কারেন্সি কনভার্সনের মেথড
    def convert(self, user):
        # কারেন্সি কোড ভ্যালিড কিনা 
        if not self.is_valid_currency(self.from_currency) or not self.is_valid_currency(self.to_currency):
            return "Invalid currency code."

        # ওপেন এক্সচেঞ্জ API ইউআরএল সোর্স কারেন্সি অনুযায়ী
        url = f"https://open.er-api.com/v6/latest/{self.from_currency}"

        try:
            # API কল করে রেসপন্স নেওয়া
            response = requests.get(url)
            data = response.json()

            # রেসপন্সে যদি success না হয়, তাহলে এরর মেসেজ দেখানো
            if data.get("result") != "success":
                return f"API error: {data.get('error-type', 'Unknown error')}"

            # টার্গেট কারেন্সির রেট বের করা
            rates = data.get("rates", {})
            if self.to_currency not in rates:
                return "Target currency not found in rates."

            rate = rates[self.to_currency]  # নির্দিষ্ট টার্গেট কারেন্সির রেট
            result = self.amount * rate     # কনভার্টেড অ্যামাউন্ট

            # লগারে কনভার্সন সেভ করা
            self.logger.log(user, f"{self.amount} {self.from_currency}", f"{result:.2f} {self.to_currency}")
            
            # রিটার্নে রেজাল্ট দেখানো
            return f"{self.amount} {self.from_currency} = {result:.2f} {self.to_currency}"

        except Exception as e:
            # কোন এরর হলে দেখানো হবে
            return f"Error fetching live rate: {str(e)}"

    # স্ট্যাটিক মেথড — কারেন্সি কোডের দৈর্ঘ্য ঠিক আছে কিনা চেক করে
    @staticmethod
    def is_valid_currency(code):
        return isinstance(code, str) and len(code) == 3


# ইউজার অ্যাকশন লগ করার 
class Logger:
    def __init__(self):
        self.logs = []  

    # লগ সেভ করার মেথড
    def log(self, user, amount, result):
        entry = f"User: {user} | Converted: {amount} → {result}"
        self.logs.append(entry)
        print("Log saved:", entry)


# মূল ফাংশন — ইউজার ইনপুট নেয় এবং কনভার্ট করে
def main():
    logger = Logger()  # Logger অবজেক্ট তৈরি

    # ইউজার ইনপুট নেয়া হচ্ছে
    user = input("Enter your name: ")
    try:
        amount = float(input("Enter amount to convert: "))
        from_currency = input("Enter source currency code (e.g., USD): ")
        to_currency = input("Enter target currency code (e.g., EUR): ")
    except ValueError:
        print("Invalid input.")
        return

    # CurrencyConverter অবজেক্ট তৈরি করে কনভার্ট মেথড কল করা
    converter = CurrencyConverter(amount, from_currency, to_currency, logger)
    print(converter.convert(user)) 

    # সব লগ দেখানো
    print("\nAll Logs:")
    for log in logger.logs:
        print(log)


# যখন ফাইল রান করা হবে তখন main() ফাংশন এক্সিকিউট হবে
if __name__ == "__main__":
    main()
