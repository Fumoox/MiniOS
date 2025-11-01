import os
import time
import threading
import random
import json
from datetime import datetime
from collections import deque
import shutil

class MiniOS:
    def __init__(self):
        self.current_user = None
        self.processes = {}
        self.next_pid = 1
        self.file_system = {}
        self.running = True
        self.command_history = deque(maxlen=10)
        self.boot_time = datetime.now()
        self.user_points = 0
        self.system_health = 100
        self.temperature = 35  # System temperature
        self.background_tasks_active = True

    def boot(self):
        """Boot up the mini OS with animations"""
        print("=" * 50)
        print("    MINI OPERATING SYSTEM")
        print("        Version 2.0")
        print("=" * 50)

        # Boot animation
        for i in range(5):
            print("Booting" + "." * (i % 4) + " " * (3 - (i % 4)))
            time.sleep(0.3)
            print("\033[F\033[K", end="")  # Clear line

        print("Initializing file system...")
        self._init_file_system()
        time.sleep(0.5)

        print("Starting system services...")
        time.sleep(0.5)

        print("Loading user interface...")
        time.sleep(0.5)

        # ASCII art boot complete
        print(r"""
   __  __ _       _    _____   _____
  |  \/  (_)     (_)  / ____| / ____|
  | \  / |_ _ __  _  | (___  | (___
  | |\/| | | '_ \| |  \___ \  \___ \
  | |  | | | | | | |  ____) | ____) |
  |_|  |_|_|_| |_|_| |_____/ |_____/
        """)
        print("System ready!")
        print()

    def _init_file_system(self):
        """Initialize enhanced file system structure"""
        self.file_system = {
            "/": {"type": "directory", "contents": {}, "created": datetime.now().isoformat()},
            "/home": {"type": "directory", "contents": {}, "created": datetime.now().isoformat()},
            "/system": {"type": "directory", "contents": {}, "created": datetime.now().isoformat()},
            "/games": {"type": "directory", "contents": {}, "created": datetime.now().isoformat()},
            "/system/readme.txt": {
                "type": "file",
                "content": "Welcome to MiniOS 2.0!\nExplore the system with 'help' command.\nEarn points by using the system!",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            },
            "/system/motd.txt": {
                "type": "file",
                "content": "Message of the Day:\nKeep learning and exploring!",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            },
            "/games/instructions.txt": {
                "type": "file",
                "content": "Available games:\n- guess: Number guessing game\n- math: Math challenge\n- maze: Text-based maze",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            }
        }

    def login(self):
        """Enhanced login system with user profiles"""
        print("🚀 Login to MiniOS 2.0")

        # Simple user database
        users = {
            "admin": "admin123",
            "user": "user123",
            "guest": "guest"
        }

        attempts = 3
        while attempts > 0:
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if username in users and users[username] == password:
                self.current_user = username
                self._create_user_directory(username)
                self._load_user_profile(username)

                # Welcome messages
                welcome_messages = [
                    f"🌟 Welcome back, {username}!",
                    f"🚀 Great to see you, {username}!",
                    f"🎯 Ready for adventure, {username}?",
                    f"💫 Hello {username}, let's explore!"
                ]
                print(random.choice(welcome_messages))
                print(f"📊 Your current points: {self.user_points}")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Login failed! {attempts} attempts remaining.")
                else:
                    print("💀 Too many failed attempts. System locked.")
                    return False

    def _create_user_directory(self, username):
        """Create user's home directory with sample files"""
        user_home = f"/home/{username}"
        if user_home not in self.file_system:
            self.file_system[user_home] = {
                "type": "directory",
                "contents": {},
                "created": datetime.now().isoformat()
            }

            # Create sample files for user
            self.file_system[f"{user_home}/welcome.txt"] = {
                "type": "file",
                "content": f"Welcome to your home directory, {username}!\n\nTips:\n- Use 'help' to see commands\n- Play games with 'game' command\n- Explore the file system with 'ls' and 'cd'",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            }

    def _load_user_profile(self, username):
        """Load or create user profile with points"""
        profile_file = f"/system/profiles/{username}.json"
        if profile_file in self.file_system:
            try:
                profile_data = json.loads(self.file_system[profile_file]["content"])
                self.user_points = profile_data.get("points", 0)
            except:
                self.user_points = 0
        else:
            self.user_points = 0

    def _save_user_profile(self, username):
        """Save user profile"""
        profile_file = f"/system/profiles/{username}.json"
        profile_data = {"points": self.user_points, "last_save": datetime.now().isoformat()}
        self.file_system[profile_file] = {
            "type": "file",
            "content": json.dumps(profile_data, indent=2),
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }

    def award_points(self, points, reason=""):
        """Award points to user for system interaction"""
        old_points = self.user_points
        self.user_points += points
        print(f"🎉 +{points} points! {reason}")
        print(f"📊 Total points: {self.user_points}")

        # Save profile when points are awarded
        if self.current_user:
            self._save_user_profile(self.current_user)

    def create_process(self, name, target_function, *args):
        """Create a new process with enhanced tracking"""
        pid = self.next_pid
        self.next_pid += 1

        process = {
            "pid": pid,
            "name": name,
            "status": "running",
            "start_time": datetime.now(),
            "cpu_usage": random.randint(1, 10),
            "memory_usage": random.randint(10, 100),
            "thread": threading.Thread(target=target_function, args=args, daemon=True)
        }

        self.processes[pid] = process
        process["thread"].start()
        print(f"🔄 Process '{name}' (PID: {pid}) started")
        return pid

    def list_processes(self):
        """Enhanced process listing with system metrics"""
        print("\n" + "="*60)
        print("📊 SYSTEM PROCESS MANAGER")
        print("="*60)
        print(f"{'PID':<6} {'Name':<15} {'Status':<10} {'CPU%':<6} {'Memory':<8} {'Uptime':<12}")
        print("-" * 60)

        active_processes = 0
        total_cpu = 0
        total_memory = 0

        for pid, process in self.processes.items():
            if process["status"] == "running":
                active_processes += 1
                total_cpu += process["cpu_usage"]
                total_memory += process["memory_usage"]
                uptime = datetime.now() - process["start_time"]
                print(f"{pid:<6} {process['name']:<15} {process['status']:<10} "
                      f"{process['cpu_usage']:<6} {process['memory_usage']:<8}MB "
                      f"{str(uptime).split('.')[0]:<12}")

        print("-" * 60)
        print(f"Total: {active_processes} processes | CPU: {total_cpu}% | Memory: {total_memory}MB")

        # Award points for checking processes
        self.award_points(2, "for system monitoring")

    def system_info(self):
        """Enhanced system information with health metrics"""
        uptime = datetime.now() - self.boot_time
        terminal_width = shutil.get_terminal_size().columns

        print("\n" + "="*terminal_width)
        print("🖥️  SYSTEM INFORMATION")
        print("="*terminal_width)

        # System metrics with emojis
        metrics = [
            ("OS Version", "MiniOS 2.0 🚀"),
            ("Boot Time", self.boot_time.strftime('%Y-%m-%d %H:%M:%S')),
            ("Uptime", str(uptime).split('.')[0]),
            ("Active Processes", f"{len([p for p in self.processes.values() if p['status'] == 'running'])} 🔄"),
            ("System Health", f"{self.system_health}% {'💚' if self.system_health > 70 else '💛' if self.system_health > 30 else '💔'}"),
            ("Temperature", f"{self.temperature}°C {'❄️' if self.temperature < 40 else '🔥' if self.temperature > 60 else '🌡️'}"),
            ("Logged in as", f"{self.current_user} 👤"),
            ("User Points", f"{self.user_points} 🏆")
        ]

        for label, value in metrics:
            print(f"{label:<20}: {value}")

        # System status message
        if self.system_health > 80:
            status_msg = "System is in excellent condition! 🌟"
        elif self.system_health > 50:
            status_msg = "System is running normally. ✅"
        else:
            status_msg = "System needs attention! ⚠️"

        print(f"\nStatus: {status_msg}")
        print("="*terminal_width)

        self.award_points(1, "for checking system info")

    def play_game(self, game_name=None):
        """Game launcher with multiple mini-games"""
        if not game_name:
            print("\n🎮 Available Games:")
            print("1. guess  - Number guessing game")
            print("2. math   - Math challenge")
            print("3. maze   - Text-based maze adventure")
            print("4. trivia - System knowledge quiz")

            choice = input("\nChoose a game (name or number): ").strip().lower()

            game_map = {
                "1": "guess", "guess": "guess",
                "2": "math", "math": "math",
                "3": "maze", "maze": "maze",
                "4": "trivia", "trivia": "trivia"
            }

            game_name = game_map.get(choice, choice)

        if game_name == "guess":
            self._game_guess_number()
        elif game_name == "math":
            self._game_math_challenge()
        elif game_name == "maze":
            self._game_maze()
        elif game_name == "trivia":
            self._game_trivia()
        else:
            print("Unknown game! Available: guess, math, maze, trivia")

    def _game_guess_number(self):
        """Number guessing game"""
        print("\n🎯 Number Guessing Game!")
        print("I'm thinking of a number between 1 and 100...")

        number = random.randint(1, 100)
        attempts = 0
        max_attempts = 7

        while attempts < max_attempts:
            try:
                guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts}: Your guess? "))
                attempts += 1

                if guess < number:
                    print("📈 Too low! Try higher.")
                elif guess > number:
                    print("📉 Too high! Try lower.")
                else:
                    points = max(10 - attempts, 1) * 5
                    print(f"🎉 Correct! You guessed it in {attempts} attempts!")
                    self.award_points(points, f"for winning guessing game in {attempts} attempts")
                    return

            except ValueError:
                print("Please enter a valid number!")

        print(f"💀 Game over! The number was {number}.")
        self.award_points(5, "for participating in guessing game")

    def _game_math_challenge(self):
        """Math challenge game"""
        print("\n🧮 Math Challenge!")
        print("Solve these math problems quickly!")

        operations = ['+', '-', '*']
        score = 0

        for round_num in range(5):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(operations)

            if op == '+':
                answer = a + b
            elif op == '-':
                answer = a - b
            else:
                answer = a * b

            start_time = time.time()
            try:
                user_answer = int(input(f"\nQ{round_num + 1}: {a} {op} {b} = ? "))
                time_taken = time.time() - start_time

                if user_answer == answer:
                    round_points = max(10 - int(time_taken), 1)
                    score += round_points
                    print(f"✅ Correct! (+{round_points} points, {time_taken:.1f}s)")
                else:
                    print(f"❌ Wrong! Answer was {answer}")

            except ValueError:
                print("❌ Please enter a valid number!")

        total_points = score * 2
        print(f"\n🏁 Game over! Final score: {score}")
        self.award_points(total_points, f"for math challenge (score: {score})")

    def _game_maze(self):
        """Simple text-based maze game"""
        print("\n🧭 Maze Adventure!")
        print("Find your way through the maze using commands: north, south, east, west")

        # Simple maze structure
        maze = {
            'start': {'east': 'room1', 'description': 'You are at the entrance. Path to EAST.'},
            'room1': {'west': 'start', 'east': 'room2', 'north': 'room3', 'description': 'Crossroads. Paths: WEST, EAST, NORTH'},
            'room2': {'west': 'room1', 'description': 'Dead end with a key! Go WEST.'},
            'room3': {'south': 'room1', 'east': 'exit', 'description': 'Path splits. Go SOUTH or EAST'},
            'exit': {'west': 'room3', 'description': 'You found the exit! 🎉'}
        }

        current_room = 'start'
        moves = 0
        has_key = False

        while current_room != 'exit':
            print(f"\n{maze[current_room]['description']}")
            move = input("Which way? ").strip().lower()

            if move in maze[current_room]:
                current_room = maze[current_room][move]
                moves += 1

                # Special events
                if current_room == 'room2' and not has_key:
                    print("🔑 You found a golden key!")
                    has_key = True

            else:
                print("❌ You can't go that way! Try another direction.")

        points = max(50 - moves * 2, 10)
        print(f"\n🎉 Congratulations! You escaped in {moves} moves!")
        if has_key:
            points += 20
            print("🔑 Bonus: You found the golden key!")

        self.award_points(points, f"for escaping maze in {moves} moves")

    def _game_trivia(self):
        """System knowledge trivia game"""
        print("\n🤔 MiniOS Trivia Challenge!")

        questions = [
            {
                "question": "What command shows running processes?",
                "options": ["A) ls", "B) ps", "C) info", "D) kill"],
                "answer": "B"
            },
            {
                "question": "Which directory contains user files?",
                "options": ["A) /system", "B) /home", "C) /root", "D) /bin"],
                "answer": "B"
            },
            {
                "question": "What does PID stand for?",
                "options": ["A) Process ID", "B) Program ID", "C) Process Index", "D) Program Index"],
                "answer": "A"
            }
        ]

        score = 0

        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}: {q['question']}")
            for option in q['options']:
                print(f"  {option}")

            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer == q['answer']:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! Correct answer was {q['answer']}")

        points = score * 15
        print(f"\n📊 You got {score}/3 correct!")
        self.award_points(points, f"for trivia knowledge ({score}/3 correct)")

    def command_help(self):
        """Enhanced help system with categories"""
        print("\n" + "="*50)
        print("🆘 MINIOS HELP SYSTEM")
        print("="*50)

        categories = {
            "📁 File System": [
                ("ls [dir]", "List directory contents"),
                ("cd [dir]", "Change directory"),
                ("create <file>", "Create new file"),
                ("read <file>", "Read file content"),
                ("delete <file>", "Delete file")
            ],
            "🔄 Process Management": [
                ("ps", "List running processes"),
                ("kill <pid>", "Terminate process"),
                ("top", "System monitor")
            ],
            "🎮 Entertainment": [
                ("game", "Play games"),
                ("weather", "Check weather"),
                ("fortune", "Random fortune")
            ],
            "ℹ️ System Info": [
                ("info", "System information"),
                ("time", "Current time"),
                ("history", "Command history"),
                ("points", "Check your points")
            ],
            "⚙️ Utilities": [
                ("clear", "Clear screen"),
                ("help", "Show this help"),
                ("exit", "Shutdown system")
            ]
        }

        for category, commands in categories.items():
            print(f"\n{category}:")
            for cmd, desc in commands:
                print(f"  {cmd:<15} {desc}")

        print(f"\n💡 Tip: Earn points by using the system!")
        print("="*50)

        self.award_points(1, "for seeking help")

    def check_weather(self):
        """Fun weather simulation"""
        weather_types = ["☀️ Sunny", "🌧️ Rainy", "⛅ Cloudy", "❄️ Snowy", "🌪️ Stormy", "🌈 Rainbow"]
        temperatures = random.randint(-5, 35)
        weather = random.choice(weather_types)

        print(f"\n🌤️  Weather Report:")
        print(f"Condition: {weather}")
        print(f"Temperature: {temperatures}°C")
        print(f"Forecast: Perfect for coding! 💻")

        self.award_points(2, "for checking weather")

    def show_fortune(self):
        """Unix-like fortune command"""
        fortunes = [
            "The code that is written today will debug you tomorrow.",
            "A bug in the code is worth two in the documentation.",
            "He who laughs last probably made a backup.",
            "There are 10 types of people: those who understand binary and those who don't.",
            "The best way to predict the future is to implement it.",
            "Keep calm and code on!",
            "Your computer will do what you tell it to do, but that may be much different from what you had in mind.",
        ]

        fortune = random.choice(fortunes)
        print(f"\n🔮 Fortune: {fortune}")
        self.award_points(1, "for seeking wisdom")

    def show_points(self):
        """Show user points and achievements"""
        print(f"\n🏆 User Profile: {self.current_user}")
        print(f"📊 Current Points: {self.user_points}")

        if self.user_points >= 100:
            rank = "🌟 Elite Coder"
        elif self.user_points >= 50:
            rank = "🚀 Advanced User"
        elif self.user_points >= 20:
            rank = "💫 Explorer"
        else:
            rank = "🌱 Beginner"

        print(f"🎯 Rank: {rank}")

        # Next milestone
        next_milestone = ((self.user_points // 25) + 1) * 25
        points_needed = next_milestone - self.user_points
        print(f"🎯 Next milestone: {next_milestone} points ({points_needed} more needed)")

    def run_command(self, command):
        """Enhanced command execution with points system"""
        if command.strip():
            self.command_history.append(command)

        parts = command.split()
        if not parts:
            return

        cmd = parts[0].lower()

        # Update system metrics randomly
        self._update_system_metrics()

        try:
            if cmd == "help":
                self.command_help()

            elif cmd == "info":
                self.system_info()

            elif cmd == "ps":
                self.list_processes()

            elif cmd == "top":
                self.list_processes()
                print("\n🔄 System monitor active... Press Ctrl+C to exit")
                try:
                    for _ in range(5):
                        time.sleep(2)
                        self._update_system_metrics()
                        # Simulate process changes
                        for process in self.processes.values():
                            if process["status"] == "running":
                                process["cpu_usage"] = random.randint(1, 15)
                                process["memory_usage"] = random.randint(5, 50)
                except KeyboardInterrupt:
                    print("\nExiting system monitor...")

            elif cmd == "kill" and len(parts) > 1:
                try:
                    pid = int(parts[1])
                    self.kill_process(pid)
                    self.award_points(3, "for process management")
                except ValueError:
                    print("❌ Invalid PID")

            elif cmd == "ls":
                directory = parts[1] if len(parts) > 1 else "/"
                self.list_files(directory)
                self.award_points(1, "for file exploration")

            elif cmd == "create" and len(parts) > 1:
                filename = parts[1]
                content = input("Enter file content: ")
                if self.create_file(filename, content):
                    self.award_points(3, "for file creation")

            elif cmd == "read" and len(parts) > 1:
                content = self.read_file(parts[1])
                if content is not None:
                    print(f"\nContent of {parts[1]}:\n{'-'*40}\n{content}\n{'-'*40}")
                    self.award_points(1, "for reading files")

            elif cmd == "delete" and len(parts) > 1:
                if self.delete_file(parts[1]):
                    self.award_points(2, "for file management")

            elif cmd == "game":
                game_name = parts[1] if len(parts) > 1 else None
                self.play_game(game_name)

            elif cmd == "weather":
                self.check_weather()

            elif cmd == "fortune":
                self.show_fortune()

            elif cmd == "time":
                print(f"🕒 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.award_points(1, "for time awareness")

            elif cmd == "history":
                print("\n📜 Command History:")
                for i, cmd in enumerate(self.command_history, 1):
                    print(f"{i:2d}: {cmd}")
                self.award_points(1, "for reviewing history")

            elif cmd == "points":
                self.show_points()

            elif cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.award_points(1, "for keeping clean")

            elif cmd == "exit":
                print("🔄 Shutting down system...")
                if self.current_user:
                    self._save_user_profile(self.current_user)
                print("💾 Profiles saved.")
                print("👋 Goodbye!")
                self.running = False

            else:
                print(f"❌ Unknown command: {cmd}")
                print("💡 Type 'help' for available commands")

        except Exception as e:
            print(f"💥 Error executing command: {e}")

    def _update_system_metrics(self):
        """Update system health metrics randomly"""
        # Random small changes to system metrics
        self.system_health += random.randint(-2, 2)
        self.system_health = max(0, min(100, self.system_health))

        self.temperature += random.randint(-1, 1)
        self.temperature = max(20, min(80, self.temperature))

    # File system methods (similar to before but enhanced)
    def list_files(self, directory="/"):
        if directory not in self.file_system:
            print(f"❌ Directory {directory} not found")
            return

        if self.file_system[directory]["type"] != "directory":
            print(f"❌ {directory} is not a directory")
            return

        print(f"\n📁 Contents of {directory}:")
        print("-" * 40)

        items = []
        for item, metadata in self.file_system.items():
            if item.startswith(directory.rstrip('/') + '/') and item != directory:
                relative_path = item[len(directory.rstrip('/')):].lstrip('/')
                if '/' not in relative_path or directory == '/':
                    items.append((relative_path, metadata))

        for item, metadata in sorted(items):
            item_type = "📁" if metadata["type"] == "directory" else "📄"
            print(f"{item_type} {item}")

    def create_file(self, path, content=""):
        if path in self.file_system:
            print(f"❌ File {path} already exists")
            return False

        self.file_system[path] = {
            "type": "file",
            "content": content,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        print(f"✅ File {path} created")
        return True

    def read_file(self, path):
        if path not in self.file_system:
            print(f"❌ File {path} not found")
            return None

        if self.file_system[path]["type"] != "file":
            print(f"❌ {path} is not a file")
            return None

        return self.file_system[path]["content"]

    def delete_file(self, path):
        if path not in self.file_system:
            print(f"❌ File {path} not found")
            return False

        if self.file_system[path]["type"] != "file":
            print(f"❌ {path} is not a file")
            return False

        del self.file_system[path]
        print(f"✅ File {path} deleted")
        return True

    def kill_process(self, pid):
        if pid in self.processes:
            self.processes[pid]["status"] = "terminated"
            print(f"🔴 Process {pid} terminated")
        else:
            print(f"❌ Process {pid} not found")

    def start_shell(self):
        """Start the enhanced command line interface"""
        print("\n💡 Type 'help' for available commands")
        print("🎮 Try 'game' to play some games!")
        print("🏆 Earn points by using the system!\n")

        # Start only essential background processes
        self.create_process("system_health", self._system_health_monitor)

        while self.running:
            try:
                # Dynamic prompt with system info
                prompt = f"\n{self.current_user}@MiniOS[{self.user_points}pts]$ "
                command = input(prompt).strip()
                self.run_command(command)

            except KeyboardInterrupt:
                print("\n\n💡 Use 'exit' command to shutdown the system")
            except EOFError:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"💥 System error: {e}")

    def _system_health_monitor(self):
        """Background system health monitoring (only runs occasionally)"""
        while self.running:
            time.sleep(30)  # Only check every 30 seconds
            if not self.running:
                break

            # Only print messages occasionally
            if random.random() < 0.3:  # 30% chance
                messages = [
                    "🔍 System scan: All services normal",
                    "💾 Memory usage: Optimal",
                    "🔄 Background tasks: Running smoothly",
                    "🌡️  System temperature: Stable"
                ]
                print(f"\n[System] {random.choice(messages)}")

def main():
    """Main function to run the enhanced MiniOS"""
    os_system = MiniOS()

    try:
        # Boot the system
        os_system.boot()

        # Login
        if not os_system.login():
            return

        # Start the shell
        os_system.start_shell()

    except Exception as e:
        print(f"💥 Fatal system error: {e}")
    finally:
        print("🛑 System shutdown complete.")

if __name__ == "__main__":
    main()
