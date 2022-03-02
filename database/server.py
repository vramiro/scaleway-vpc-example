from socketserver import TCPServer, BaseRequestHandler
import random

HOST = 'localhost'
PORT = 4242

quotes = [
"1|It is not in the stars to hold our destiny but in ourselves|William Shakespeare",
"2|Good artists copy, great artists steal|Pablo Picasso",
"3|The time is always right to do what is right|Martin Luther King",
"4|Be the change that you wish to see in the world|Mahatma Gandhi",
"5|Integrity is doing the right thing, even when no one is watching|C. S. Lewis",
"6|An eye for an eye will only make the whole world blind|Mahatma Gandhi",
"7|Out of difficulties grow miracles|Jean de la Bruyere",
"8|The journey of a thousand miles begins with one step|Lao Tzu",
"9|You can't blame gravity for falling in love|Albert Einstein",
"10|Insanity: doing the same thing over and over again and expecting different results|Albert Einstein",
"11|All our dreams can come true, if we have the courage to pursue them|Walt Disney",
"12|Giving up smoking is the easiest thing in the world. I know because I've done it thousands of times|Mark Twain",
"13|Patriotism is supporting your country all the time, and your government when it deserves it|Mark Twain",
"14|Stay hungry, stay foolish|Steve Jobs",
"15|Things do not happen. Things are made to happen|John F. Kennedy",
"16|To hold a pen is to be at war|Voltaire",
"17|Understanding is a two-way street|Eleanor Roosevelt",
"18|Fate loves the fearless|James Russell Lowell",
"19|Knowledge comes, but wisdom lingers|Alfred Lord Tennyson",
"20|A friend in power is a friend lost|Henry Adams",
"21|Life is an adventure in forgiveness|Norman Cousins",
"22|The truth is rarely pure and never simple|Oscar Wilde",
"23|When the gods wish to punish us they answer our prayers|Oscar Wilde",
"24|Always forgive your enemies - nothing annoys them so much|Oscar Wilde",
"25|A will finds a way|Orison Swett Marden",
"26|Knowledge is power|Francis Bacon",
"27|Courage is found in unlikely places|J. R. R. Tolkien",
"28|If you don’t stand for something, you’ll fall for anything|Alexander Hamilton",
"29|Choose a job you love, and you will never have to work a day in your life|Confucius",
"30|Freedom lies in being bold|Robert Frost",
"31|Life is a dream for the wise, a game for the fool, a comedy for the rich, a tragedy for the poor|Sholom Aleichem"
]

class QOTDRequestHandler(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(0).strip()
        print("Connection from {}".format(self.client_address[0]))
        self.request.sendall(bytes(random.choice(quotes).encode('utf-8')))

if __name__ == "__main__":
    with TCPServer((HOST, PORT), QOTDRequestHandler) as s:
        print("Server started at %s:%s" % (HOST, PORT))
        s.serve_forever()