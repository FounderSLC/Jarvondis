from jarvondis import Jarvondis
from runtime.panther_surface import PantherSurface


def main():
    """
    Tiny local CLI for Jarvondis.
    Behaves like a lightweight Copilot console.
    """

    j = Jarvondis()
surface = PantherSurface(j)

j.initialize()

print("\n🔵 Panther-OS Command Surface online.")
print("Type 'exit' or 'quit' to close.\n")

while True:
    try:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("🟣 Panther-OS shutting down. Safe travels, Captain.")
            break

        # Route through Panther-OS command surface
        response = surface.execute(user_input)
        print(f"Panther-OS: {response}\n")

    except KeyboardInterrupt:
        print("\n🟣 Interrupted. Panther-OS powering down.")
        break

    except Exception as e:
        print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    main()
