# main.py
# Simple In-Memory CLI Todo App (Phase I)

todos = []
next_id = 1

def add_todo():
    global next_id
    title = input("Enter title: ")
    desc = input("Enter description: ")
    todos.append({
        "id": next_id,
        "title": title,
        "description": desc,
        "completed": False
    })
    print(f"Todo added with ID {next_id}")
    next_id += 1

def view_todos():
    if not todos:
        print("No todos yet.")
        return
    for t in todos:
        status = "✅" if t["completed"] else "❌"
        print(f'{t["id"]}: {t["title"]} - {t["description"]} [{status}]')

def update_todo():
    tid = int(input("Enter ID to update: "))
    for t in todos:
        if t["id"] == tid:
            t["title"] = input(f"New title (current: {t['title']}): ") or t["title"]
            t["description"] = input(f"New description (current: {t['description']}): ") or t["description"]
            print("Todo updated.")
            return
    print("Todo ID not found.")

def delete_todo():
    tid = int(input("Enter ID to delete: "))
    global todos
    for t in todos:
        if t["id"] == tid:
            todos = [x for x in todos if x["id"] != tid]
            print("Todo deleted.")
            return
    print("Todo ID not found.")

def mark_complete():
    tid = int(input("Enter ID to mark complete/incomplete: "))
    for t in todos:
        if t["id"] == tid:
            t["completed"] = not t["completed"]
            print(f"Todo marked as {'complete' if t['completed'] else 'incomplete'}.")
            return
    print("Todo ID not found.")

def main():
    while True:
        print("\n--- Todo CLI ---")
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            add_todo()
        elif choice == "2":
            view_todos()
        elif choice == "3":
            update_todo()
        elif choice == "4":
            delete_todo()
        elif choice == "5":
            mark_complete()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
