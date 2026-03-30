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

- Did your design change during implementation? Yes
- If yes, describe at least one change and why you made it.
Yes, my design changed quite a bit during implementation. The biggest change was moving tasks from the Planner class into the Pet class. In my original UML, the Planner held a flat list of all tasks. But when I started actually writing the code, I realized it makes more sense for each pet to own its own tasks, because a walk belongs to Mochi, not to the schedule. This made the whole system feel more natural and easier to reason about.

I also renamed Planner to Scheduler because the class was doing more than just planning which was sorting, filtering, detecting conflicts, and managing recurring tasks. Scheduler felt like a more accurate name for what it actually does.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler considers two main constraints: available time (how many minutes the owner has today) and task priority (high, medium, or low). I also store scheduled_time and due_date on each task, but those are used for display and sorting rather than for deciding what gets included in the plan.

- How did you decide which constraints mattered most?
I decided priority mattered most because in pet care, some things are simply non-negotiable which feeding and medication have to happen no matter what. Time is the second constraint because the owner only has so many hours in a day. I chose not to make frequency affect the priority score because I thought it would make the logic too complicated, and priority already captures urgency well enough.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler uses a greedy approach which always picks the highest priority task first, then keeps adding tasks until the time runs out. This means it does not try every possible combination of tasks to find the most efficient schedule. For example, if two high-priority tasks together take 80 minutes but the owner only has 60 minutes, the scheduler will try to fit them both and then have no time left for anything else, even if a medium-priority task only takes 5 minutes and could easily fit.

- Why is that tradeoff reasonable for this scenario?
For a pet care app, I think this tradeoff is reasonable because the most important thing is to make sure critical tasks like feeding and medication always happen first. A more "optimal" algorithm that tries every combination would be more complex to write and harder to understand, and for daily pet care the difference is usually small. The owner also knows their pet's needs best, if they mark something as high priority, the scheduler should respect that without question. So being simple and predictable is more useful here than being mathematically perfect.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI tools in almost every phase of this project. At the beginning, I used it to brainstorm what classes I needed and what responsibilities each one should have. During implementation, I asked it to help me write method stubs and flesh out the logic for things like generate_plan() and next_occurrence(). I also used it for debugging when I wasn't sure why the filter wasn't showing all tasks.

- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific ones like "given this Task class, write a method that returns a new Task due one day later based on frequency" rather than general ones. When I gave context about what I already had, the suggestions were much more useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment I did not accept the AI suggestion as-is was when it first generated the explain_plan() method to group tasks by pet. The AI organized the output in sections like "Mochi's tasks:" and "Luna's tasks:" but I realized that was not what I wanted. A pet owner needs to see tasks ranked by priority across all pets, not grouped by pet. I changed it to a flat numbered list sorted by priority, with the pet name shown inline for each task. 

- How did you evaluate or verify what the AI suggested?
I verified it by reading through the output manually and thinking about what I would actually want to see if I were Jordan planning my morning.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion (does mark_complete() actually flip the flag?), task addition (does adding a task increase the pet's task count?), sorting correctness (do tasks come out in chronological order after sort_tasks_by_time()?), recurrence logic (does a daily task produce a next occurrence due tomorrow?), conflict detection (do two tasks at the same time trigger a warning?), and edge cases like a pet with no tasks or an owner with zero available time.

- Why were these tests important?
Because the scheduler's behavior depends on all of these working correctly together. If get_priority_score() returned wrong numbers, the whole plan would be in the wrong order. If next_occurrence() calculated the wrong date, recurring tasks would silently pile up on the wrong days.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I would say 4 out of 5. The core features are well tested and I feel confident about the happy paths. 

- What edge cases would you test next if you had more time?
There are still some edge cases I did not test like what happens if the owner has no pets at all, or if someone marks a recurring task complete twice by accident. Those are the cases I would add next if I had more time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the recurring task logic. The combination of due_date, timedelta, and next_occurrence() felt elegant,one method does exactly one thing and the result is that the owner never has to re-add a daily task manually. It also made me realize how powerful Python's datetime library is for this kind of problem.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would redesign how scheduled_time works. Right now it is just a plain string like "08:00" and I sort it using string comparison, which works but is not technically correct (it works by accident because of the HH:MM format). I would change it to use Python's datetime.time object so comparisons are actually safe and I could also calculate whether tasks overlap in duration, not just whether they start at exactly the same minute.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The most important thing I learned is that AI is very good at writing code but not always good at understanding what you actually want. Many times the AI gave me working code that did not match my real intention like grouping tasks by pet when I wanted them ranked by priority. I learned to always read the output carefully and ask myself "is this what I actually meant?" before accepting it. Good system design requires human judgment, not just correct syntax.

- What I learned about being the "lead architect":
The biggest lesson was that AI is a very fast coder but a very poor decision-maker. It can generate ten methods in one minute, but it does not know which ones you actually need, or whether they fit the design you are building toward. I had to stay in charge of the overall structure, things like deciding that tasks should live in Pet instead of Scheduler, or that the output should be ranked by priority instead of grouped by pet. Those decisions required me to think about the user experience, not just the syntax. AI helped me build faster, but I had to decide what to build.