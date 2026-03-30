# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

At first, I am thinking about three core user actions:
1. Add a pet: The user can enter their pet's basic information (name and species) so the system knows what kind of care tasks are relevant.
2. Add a care task: The user can create a task by providing a description, how long it will take, and how important it is (priority). This lets the planner know what needs to get done.
3. Generate today's plan: The user can click a button to see an ordered schedule for the day. The planner will pick and sort tasks based on priority and the owner's available time.

- Briefly describe your initial UML design.
For my initial UML design, I decided to use four main classes: Owner, Pet, Task, and Planner. The relationships between classes are: Owner has one or more Pets, and Planner uses the Owner, a list of Pet objects, and a list of Task objects to build the schedule.

- What classes did you include, and what responsibilities did you assign to each?
1. Owner: stores the owner's name, their daily time limit, and their personal preferences (like preferred walk time or what kind of tasks they care most about).
2. Pet: stores the pet's name, species, and any special needs (for example, a dog needs more frequent walks than a cat).
3. Task: represents one care activity. It has a title, a description, how long it takes (duration), how often it should happen (frequency), and a priority level (high, medium, or low).
4. Planner: is the main scheduling class. It takes a list of tasks and the constraints from the owner and pet, then produces an ordered daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler uses a greedy approach which always picks the highest priority task first, then keeps adding tasks until the time runs out. This means it does not try every possible combination of tasks to find the most efficient schedule. For example, if two high-priority tasks together take 80 minutes but the owner only has 60 minutes, the scheduler will try to fit them both and then have no time left for anything else, even if a medium-priority task only takes 5 minutes and could easily fit.

- Why is that tradeoff reasonable for this scenario?
For a pet care app, I think this tradeoff is reasonable because the most important thing is to make sure critical tasks like feeding and medication always happen first. A more "optimal" algorithm that tries every combination would be more complex to write and harder to understand, and for daily pet care the difference is usually small. The owner also knows their pet's needs best, if they mark something as high priority, the scheduler should respect that without question. So being simple and predictable is more useful here than being mathematically perfect.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
