import sys
from jarvondis import Jarvondis

def main():
    """
    Tiny local CLI for Jarvondis.
    Behaves like a lightweight Copilot console.
    """

    j = Jarvondis()
    j.initialize()

    print("\n🔵 Jarvondis CLI online.")
    print("Type 'exit' or 'quit' to close.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ("exit", "quit"):
                print("🟣 Jarvondis shutting down. Safe travels, Captain.")
                break

            response = j.respond(user_input)
            print(f"Jarvondis: {response}\n")

        except KeyboardInterrupt:
            print("\n🟣 Interrupted. Jarvondis powering down.")
            break

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
