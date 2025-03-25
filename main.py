from workflows.simple_plan_and_schedule import GoalExecutionWorkflow

if __name__ == "__main__":
    workflow = GoalExecutionWorkflow(model_name="mistral")

    print("Choose:")
    print("1. Plan a new goal")
    print("2. Daily task check-in")
    print("3. Weekly summary")
    choice = input("Your choice: ")

    if choice == "1":
        goal = input("What’s your goal? ")
        workflow.run(goal)

    elif choice == "2":
        workflow.run_daily_checkin_all()

    elif choice == "3":
        workflow.send_weekly_summary()
