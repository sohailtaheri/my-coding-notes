---
title: "Turn Claude into the ultimate personal trainer (full guide)"
source: "https://x.com/Hawks0x/status/2039438255653806526"
author:
  - "[[@Hawks0x]]"
published: 2026-03-29
created: 2026-04-06
description: "Making progress in the gym and building your dream physique has never been easier.A few years back we'd spend hours watching YouTube tutoria..."
tags:
  - "clippings"
---

## Go to claude.ai

- Sign up for a free account if you haven't already.
- On the left sidebar, hit **"Projects"** - **"New Project"**
- Name it whatever you want. I called mine HAWKS PT, under the name just put what your goals are.
- Here's where most people go wrong:
	- Inside your Project, there's a section called **"Project"** and **''Files''** This is where you tell Claude assistant exactly who it is and how to behave.
	- Without it feeding it this information, Claude is just a chatbot. With it, it becomes your own tailored PT.

## Instructions

Edit the marked fields with your own stats and paste it into the instructions section:

**New to the gym? Leave the working weights blank and set your experience level to Beginner. Claude will start you light and use your first week to establish your baseline.**

```text
IDENTITY
 
You are a personal trainer AI built specifically for Sohail. You are direct,
knowledgeable, and evidence-based. No fluff — talk like a coach who actually
trains. Adapt your tone to the athlete over time.
 
-------------------------------------
ATHLETE PROFILE
-------------------------------------
 
Name: Sohail Taheri
Training experience: intermediate
Goal: General fitness, Muscel Gain
Schedule: 4 days per week
Equipment access: Commercial gym
Injuries or limitations: [e.g. None / Bad left shoulder / Lower back issues]
 
-------------------------------------
CURRENT WORKING WEIGHTS
-------------------------------------
 
These are the athlete's current working weights — the actual weights lifted
in sessions. These are NOT one rep maxes. Do not calculate percentages from
these numbers. Use them as the starting point and apply RPE-based progression
only.
 
For any exercise not listed here, refer to the lift log. If no log entry
exists yet, make a reasonable estimate, flag it as a calibration weight,
and confirm the actual weight after session 1.
 
CHEST
Barbell Bench Press:       5 — kg

BACK
Lat Pulldown:              15 — kg
 
SHOULDERS
Lateral Raise (DB):        5 — kg
 
ARMS
Barbell Curl:             10  — kg
Tricep Pushdown (cable):  13  — kg
 
Legs
Squat - KG
Leg curl - KG
Romanian Deadlift:          — kg
 
Update individual entries whenever a working weight increases.
 
-------------------------------------
LIFT LOG
-------------------------------------
 
Each session the athlete logs should be appended here in this format:
 
[DATE] — Session Name
Exercise | Sets x Reps | Weight | RPE | Notes
---
Session notes: [how it felt, energy, anything notable]
 
Never delete old entries — they are the source of truth for all exercise
weights and progress tracking. After a few sessions, the log takes over
from the working weights above as the primary reference.
 
-------------------------------------
PROGRAMMING RULES
-------------------------------------
 
- Use RPE-based loading (RPE 7-8 for hypertrophy work, 8-10 for strength work)
- Never calculate working weights from percentages — always use the logged
  working weights as the baseline
- Progressive overload: add weight when the athlete hits the top of a rep
  range at target RPE for 2 consecutive sessions
  Upper body compounds: add 2.5 kg
  Lower body compounds: add 5 kg
  Accessories: add reps before adding weight
- Suggest a deload every 4-6 weeks or when fatigue or stalling is flagged
- Prioritise compound movements. Use accessories to address weak points
- Treat Week 1 of any new programme as a calibration week — flag anything
  that needs adjusting before Week 2
- Base each new session on the most recent log entries
 
-------------------------------------
HOW TO RESPOND
-------------------------------------
 
- When the athlete logs a session: acknowledge it, update the log, note any
  weight increases, and flag anything worth adjusting
- When asked for the next session: programme it with specific weights, sets,
  reps and RPE targets based on the log
- When asked about progress: pull from the log and give concrete numbers
  and trends
- Keep responses concise. Use tables for session programming. No waffle.
 
=====================================
END OF INSTRUCTIONS
=====================================
```

## Files

We now have three files to paste in, the first one you'll need to spend around five minutes filling out which exercises you enjoy and what to include in your workouts.

This is the most important part of the setup as you want the workouts to be tailored to you.

The other two files you can paste straight in no need at all to change them, our Claude assistant will fill them in as it learns more about you.

### Name: Exercise library

```text
=====================================
EXERCISE LIBRARY
=====================================
 
Exercise Status:
  [YES]  — can do, happy to include
  [SUB]  — can do but prefer a substitute
  [NO]   — injury, equipment, or preference — do not programme
 
-------------------------------------
LOWER BODY — QUAD DOMINANT
-------------------------------------
 
Barbell Back Squat        [YES]
Barbell Front Squat       [SUB]
Safety Bar Squat          [YES]
Hack Squat (machine)      [YES]
Leg Press                 [YES]
Bulgarian Split Squat     [YES]
Lunges (barbell/DB)       [NO]
Step Ups                  [YES]
Goblet Squat              [SUB]
Leg Extension (machine)   [YES]
 
-------------------------------------
LOWER BODY — POSTERIOR CHAIN
-------------------------------------
 
Conventional Deadlift     [YES]
Sumo Deadlift             [NO]
Romanian Deadlift         [NO]
Stiff Leg Deadlift        [NO]
Hip Thrust (barbell)      [NO]
Hip Thrust (machine)      [YES]
Glute Bridge              [YES]
Leg Curl (lying)          [YES]
Leg Curl (seated)         [YES]
Nordic Curl               [NO]
Good Morning              [YES]
Cable Pull Through        [YES]
 
-------------------------------------
UPPER BODY — PUSH (HORIZONTAL)
-------------------------------------
 
Barbell Bench Press       [YES]
Dumbbell Bench Press      [YES]
Incline Barbell Press     [YES]
Incline Dumbbell Press    [YES]
Decline Press             [SUB]
Machine Chest Press       [YES]
Cable Fly                 [SUB]
Dumbbell Fly              [YES]
Pec Dec (machine)         [YES]
 
-------------------------------------
UPPER BODY — PUSH (VERTICAL)
-------------------------------------
 
Barbell OHP               [YES]
Dumbbell OHP              [YES]
Arnold Press              [YES]
Seated Machine Press      [YES]
Landmine Press            [YES]
Lateral Raise (DB)        [YES]
Lateral Raise (cable)     [YES]
Rear Delt Fly (DB)        [YES]
Rear Delt Fly (machine)   [YES]
Face Pull (cable)         [YES]
 
-------------------------------------
UPPER BODY — PULL (HORIZONTAL)
-------------------------------------
 
Barbell Bent Over Row     [NO]
Dumbbell Row              [YES]
Cable Row (seated)        [YES]
Machine Row               [YES]
Chest Supported Row       [YES]
Meadows Row               [YES]
Pendlay Row               [YES]
 
-------------------------------------
UPPER BODY — PULL (VERTICAL)
-------------------------------------
 
Pull Up (bodyweight)      [NO]
Weighted Pull Up          [YES]
Chin Up                   [YES]
Lat Pulldown (bar)        [YES]
Lat Pulldown (neutral)    [YES]
Single Arm Pulldown       [YES]
Straight Arm Pulldown     [YES]
 
-------------------------------------
ARMS
-------------------------------------
 
Barbell Curl              [YES]
Dumbbell Curl             [YES]
Incline Dumbbell Curl     [YES]
Cable Curl                [YES]
Hammer Curl               [YES]
Preacher Curl (machine)   [YES]
Close Grip Bench Press    [YES]
Tricep Pushdown (cable)   [YES]
Overhead Tricep Ext (cable)[YES]
Skull Crushers            [YES]
Dips (tricep)             [YES]
 
-------------------------------------
CORE
-------------------------------------
 
Plank                     [NO]
Cable Crunch              [NO]
Hanging Leg Raise         [NO]
Ab Wheel                  [NO]
Pallof Press              [NO]
Landmine Rotation         [NO]
 
-------------------------------------
CALVES
-------------------------------------
 
Standing Calf Raise       [YES]
Seated Calf Raise         [YES]
Leg Press Calf Raise      [YES]
 
-------------------------------------
NOTES & PREFERENCES
-------------------------------------
 
Injuries / limitations:
I have varicose vains, so heave workout pushing the blood flow down the body will make trouble for me. That is why I avoid the likes of core exercies and lunges.
 
=====================================
END OF EXERCISE LIBRARY
=====================================
```

### Name: Lift log

**(Don't edit just paste)**

```text
=====================================
LIFT LOG
=====================================
 
ATHLETE: Sohail Taheri
LOG START DATE: [DD/MM/YYYY]
 
HOW TO USE:
- Paste each session below after you train
- Never delete old entries
- Upload this file to your Claude Project so it can track your progress
- Ask Claude to update your working weights and flag trends
 
-------------------------------------
CURRENT WORKING WEIGHTS
-------------------------------------
 
These are your current working weights — the actual weights you lift
in sessions. Update these whenever a weight increases.
 
Squat:        — kg  (last updated: —)
Bench Press:  — kg  (last updated: —)
Deadlift:     — kg  (last updated: —)
OHP:          — kg  (last updated: —)
[Other]:      — kg  (last updated: —)
 
-------------------------------------
SESSION LOG
-------------------------------------
 
FORMAT TO USE:
 
[DD/MM/YYYY] — [Session Name]
Week [X] | Block [1/2/3]
 
Exercise          | Sets x Reps | Weight (kg) | RPE | Notes
----------------------------------------------------------
[Exercise name]   | 4 x 6       | 100         | 8   |
[Exercise name]   | 3 x 10      | 60          | 7   |
[Exercise name]   | 3 x 12      | 40          | 7   |
 
Session notes: [Energy / sleep / how it felt / anything notable]
 
----------------------------------------------------------
 
[PASTE YOUR SESSIONS BELOW THIS LINE]
 
=====================================
END OF LOG
=====================================
```

### Name: 12 week programme template

**(Don't edit just paste)**

```text
-------------------------------------
WORKING WEIGHT LOG — TRACK EACH BLOCK
-------------------------------------
 
Record your working weight at the start and end of each block.
This shows real progress over time.
 
              | Start | End Wk4 | End Wk8 | End Wk11
Squat         |       |         |         |
Bench Press   |       |         |         |
Deadlift      |       |         |         |
OHP           |       |         |         |
[Other]       |       |         |         |
 
-------------------------------------
NOTES & ADJUSTMENTS LOG
-------------------------------------
 
Week 1:  [Calibration week — note anything too light or too heavy]
Week 2:
Week 3:
Week 4:  [End of Block 1 — how is recovery? Any stalls?]
Week 5:
Week 6:
Week 7:
Week 8:  [End of Block 2 — check working weights vs start]
Week 9:
Week 10:
Week 11:
Week 12: [Deload — assess full programme, plan next cycle]
 
=====================================
END OF TEMPLATE
=====================================
```

## Project complete

Our PT is ready. It knows your stats, your goals, and how to talk to you. From here, every conversation you have with it is a step closer to where you want to be this summer.

And it's available 24/7. Now it's time to actually use it.

## The Six Prompt Stack

Now we've set up our Project, we need to give some prompts to kick start the programme.

### Prompt one: First time setup

Use this as your very first message in the Project. It gets Claude to read everything you've uploaded and confirm it's ready to go.

```text
Read my exercise library, lift log, and programme template. 
Acknowledge what you know about me so far and flag
 anything missing from my profile before we start building my programme.
```

### Prompt two: Build your programme

```text
Based on my profile, goals, and exercise library, 
build me a full 4 day training programme. 
Use block periodisation — 
4 weeks building volume, 4 weeks increasing intensity, 
3 weeks going heavy, 1 week deload. 
Give me Day 1 in full with exercises, sets, reps, 
working weights and RPE targets. 
Then outline the structure for Days 2, 3 and 4.
```

### Prompt three: Beginner starting point

If you're new to the gym and left the ''current lifting weight'' section on instructions blank, use this prompt to get a beginners plan.

```text
I'm new to the gym and have no established 
working weights yet. Build me a beginner-friendly 
4 day programme, start everything conservatively, 
and use Week 1 to find my working weights. 
Walk me through what to expect in the first month.
```

> **These next three prompts are to be used as and when needed.**

### Prompt four: Swap an exercise

```text
I want to swap out [exercise] from my programme. 
Based on my exercise library, what's the best 
replacement that hits the same muscle group 
and fits my current block? Update the programme going forward.
```

### Prompt five: Deload week

```text
I need a deload this week. 
Based on my current programme, 
give me a full deload week — same exercises 
but adjusted volume and intensity. 
I want to recover properly without losing momentum.
```

### Prompt six: Plateau buster

```text
My [lift] has been stuck at [weight] for [X] 
sessions. Look at my log and tell me why 
you think it's stalled, then give me a 3 
week plan to break through it.
```

81 days until summer. You've got the project, you've got the setup, you've got zero excuses left.

A PT in your pocket, 24/7. For free.

Put the work in on your end too. Bad workouts, wrong weights, exercises you can't stand, tell it everything.

The more you put in, the more you get out.

## Lastly...

If you enjoy my content I appreciate anyone who signs up for my free newsletter where I post all Fitness/AI alpha.

> 29 Mar
> 
> http://thehawknest.substack.com