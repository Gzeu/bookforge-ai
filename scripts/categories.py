#!/usr/bin/env python3
"""
BookForge AI — Genre Category Library
Covers 20 major KDP genres with:
  - Sub-genre list
  - 5 premise templates per genre
  - KDP keywords
  - Recommended chapter count
  - Typical price point
  - AI generation tips
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Genre:
    id: str
    name: str
    emoji: str
    description: str
    sub_genres: list[str]
    premise_templates: list[str]
    kdp_keywords: list[str]
    recommended_chapters: int
    typical_price: float
    generation_tip: str
    color: str  # tailwind color class for UI


GENRES: dict[str, Genre] = {
    "thriller": Genre(
        id="thriller",
        name="Thriller",
        emoji="🔪",
        description="High-stakes suspense, conspiracies, and race-against-time plots.",
        sub_genres=["Political Thriller", "Psychological Thriller", "Legal Thriller",
                    "Tech Thriller", "Spy Thriller", "Medical Thriller", "Financial Thriller"],
        premise_templates=[
            "A {protagonist}, {age}, discovers that {organization} has been secretly {conspiracy} for {timeframe}. With only {deadline} before {catastrophe}, they must {goal} while evading {antagonist} who will stop at nothing.",
            "When {protagonist} receives a {trigger} containing proof that {revelation}, they become the target of {antagonist}. Set in {setting}, the clock ticks as {stakes}.",
            "A routine {job} turns into a nightmare when {protagonist} stumbles upon {secret}. Now hunted by {antagonist}, they must {goal} before {deadline} or {consequence}.",
            "Former {background} {protagonist} is pulled back into danger when {inciting_event}. The trail leads to {location} and a conspiracy that reaches the highest levels of {institution}.",
            "In {year}, {protagonist} uncovers evidence that {revelation}. With {antagonist} closing in and {complication}, they have one chance to {goal} and expose the truth.",
        ],
        kdp_keywords=["thriller novel", "suspense fiction", "conspiracy thriller", "page turner",
                      "psychological suspense", "spy thriller book", "political thriller"],
        recommended_chapters=18,
        typical_price=3.99,
        generation_tip="Keep each chapter ending on a cliffhanger. Alternate POV between protagonist and antagonist for tension."
    ),

    "romance": Genre(
        id="romance",
        name="Romance",
        emoji="❤️",
        description="Emotional love stories with a satisfying happily-ever-after.",
        sub_genres=["Contemporary Romance", "Historical Romance", "Paranormal Romance",
                    "Romantic Suspense", "Small Town Romance", "Second Chance Romance",
                    "Billionaire Romance", "Sports Romance", "Enemies to Lovers"],
        premise_templates=[
            "{protagonist_f}, a {job_f} from {hometown}, never expected to fall for {protagonist_m}, the {job_m} who just {arrival}. Their worlds collide when {inciting_event}, forcing them to work together despite {conflict}.",
            "After {backstory}, {protagonist} swears off love — until {love_interest} walks into their life at the worst possible moment. Set in {setting}, their {relationship_dynamic} romance unfolds as {external_conflict} threatens everything.",
            "Small-town {job} {protagonist} and big-city {job_2} {love_interest} are forced to {situation} together. What starts as {initial_dynamic} slowly becomes something neither expected.",
            "{protagonist} and {love_interest} were {past_relationship} years ago. When they're thrown together again by {circumstance}, old feelings resurface — but {obstacle} stands between them and a second chance.",
            "A {holiday} in {setting} was supposed to be about {goal}. Then {protagonist} met {love_interest} and everything changed. A enemies-to-lovers story about {theme}.",
        ],
        kdp_keywords=["romance novel", "love story", "contemporary romance", "small town romance",
                      "second chance romance", "enemies to lovers", "happily ever after"],
        recommended_chapters=20,
        typical_price=2.99,
        generation_tip="Focus on emotional beats and internal monologue. Include a black moment at 75% of the story before the resolution."
    ),

    "fantasy": Genre(
        id="fantasy",
        name="Fantasy",
        emoji="✨",
        description="Magic, mythical worlds, epic quests, and chosen heroes.",
        sub_genres=["Epic Fantasy", "Urban Fantasy", "Dark Fantasy", "LitRPG",
                    "Portal Fantasy", "Sword & Sorcery", "Cozy Fantasy", "Progression Fantasy"],
        premise_templates=[
            "In the realm of {world_name}, where {magic_system} governs all life, {protagonist} discovers they possess {rare_power} — the only ability that can stop {antagonist} from {dark_plan}. Their quest takes them across {locations} and forces them to question {theme}.",
            "{protagonist}, a {mundane_job} in {city}, discovers that {revelation_about_world}. Dragged into a conflict between {faction_a} and {faction_b}, they must master {skill} before the {event} destroys everything.",
            "The ancient prophecy spoke of {prophecy}. {protagonist} never believed it applied to them — until {inciting_event} left them as the last hope against {antagonist}'s {dark_plan}.",
            "When {protagonist} crosses the boundary into {other_world}, they find a world where {world_rule}. To return home, they must {quest} while navigating the politics of {factions}.",
            "A world where {magic_system} is fueled by {cost}. {protagonist}, once {background}, discovers that {secret_about_magic} — knowledge that makes them a target for both {faction_a} and {faction_b}.",
        ],
        kdp_keywords=["fantasy novel", "epic fantasy", "magic system", "fantasy adventure",
                      "chosen one fantasy", "world building fantasy", "fantasy series book 1"],
        recommended_chapters=22,
        typical_price=3.99,
        generation_tip="Establish the magic system rules in chapter 1-2. The protagonist should fail before succeeding. End with a hook for book 2."
    ),

    "scifi": Genre(
        id="scifi",
        name="Science Fiction",
        emoji="🚀",
        description="Future worlds, technology, space exploration, and humanity's fate.",
        sub_genres=["Space Opera", "Cyberpunk", "Hard Sci-Fi", "Post-Apocalyptic",
                    "Dystopian", "Time Travel", "First Contact", "Military Sci-Fi", "Solarpunk"],
        premise_templates=[
            "In {year}, humanity has {achievement}. When {protagonist}, a {job}, discovers that {revelation}, it threatens to unravel the fragile peace between {factions}. A race across {setting} to {goal} before {antagonist} triggers {catastrophe}.",
            "The colony ship {ship_name} has been traveling for {years} years when {protagonist} wakes from cryo-sleep to find {crisis}. With {timeframe} until {deadline}, they must {goal} using only {resources}.",
            "{protagonist} works for {corporation} in a world where {tech_element} has changed everything. When they discover {conspiracy}, the only ally they can trust is {unlikely_ally}. A cyberpunk story about {theme}.",
            "First contact was supposed to be {expectation}. Instead, when the {alien_species} arrived at {location}, they brought {reality}. {protagonist}, the only human who can {ability}, stands between war and peace.",
            "After {apocalyptic_event}, {protagonist} leads a group of {number} survivors across {wasteland} searching for {goal}. But the biggest threat isn't the {external_danger} — it's {human_conflict}.",
        ],
        kdp_keywords=["science fiction novel", "space opera", "cyberpunk fiction", "dystopian novel",
                      "sci-fi thriller", "post-apocalyptic fiction", "hard science fiction"],
        recommended_chapters=20,
        typical_price=3.99,
        generation_tip="Ground the sci-fi elements in real science where possible. The technology should create plot problems, not solve them."
    ),

    "mystery": Genre(
        id="mystery",
        name="Mystery",
        emoji="🔍",
        description="Whodunits, detective stories, and puzzles to solve.",
        sub_genres=["Cozy Mystery", "Police Procedural", "Amateur Sleuth", "Hard-Boiled",
                    "Historical Mystery", "Nordic Noir", "Locked Room Mystery"],
        premise_templates=[
            "{protagonist}, a {job} in the quiet town of {town}, discovers {victim}'s body in {location}. What looks like {initial_assumption} quickly reveals itself to be murder — and everyone in {town} had a reason to want {victim} dead.",
            "When {protagonist} investigates {case}, they uncover a connection to a {timeframe}-year-old {cold_case}. The deeper they dig, the more people end up dead — and the killer is someone no one would ever suspect.",
            "Retired {job} {protagonist} thought they were done with {profession}. Then {inciting_event} and they find themselves back in the game, this time investigating {case} in {setting}.",
            "The {event} at {location} killed {number} people. Police ruled it {official_verdict}, but {protagonist} knows {reason_to_doubt}. A {timeframe} investigation that will shake {institution} to its core.",
            "{protagonist} wakes up with no memory of {timeframe} and the police telling them they're the prime suspect in {crime}. They have {deadline} to prove their innocence by finding the real killer.",
        ],
        kdp_keywords=["mystery novel", "cozy mystery", "detective fiction", "whodunit",
                      "murder mystery", "amateur sleuth", "crime fiction"],
        recommended_chapters=16,
        typical_price=2.99,
        generation_tip="Plant at least 3 red herrings. The clues that solve the case should be visible to the reader from chapter 3 onward."
    ),

    "horror": Genre(
        id="horror",
        name="Horror",
        emoji="👻",
        description="Fear, dread, supernatural terror, and psychological darkness.",
        sub_genres=["Supernatural Horror", "Psychological Horror", "Cosmic Horror",
                    "Slasher", "Gothic Horror", "Body Horror", "Haunted House", "Folk Horror"],
        premise_templates=[
            "When {protagonist} moves to {location}, they begin experiencing {phenomenon}. Locals refuse to talk about {secret}. As the {events} escalate, {protagonist} uncovers the horrifying truth about {dark_history}.",
            "{protagonist} and {companions} are stranded in {isolated_location} when {supernatural_element} begins picking them off one by one. The only way to survive is to understand {ancient_evil}'s rules.",
            "A {job} in {location} seemed like the opportunity of a lifetime. But when {protagonist} discovers {revelation}, they realize the {institution} hides a history of {horror}. Now they know too much to leave alive.",
            "{protagonist} starts seeing {visions} after {triggering_event}. Doctors say it's {medical_explanation}. But the visions are real — and they're leading toward {climax}.",
            "The {object} was found in {location} and brought to {setting}. Within days, {protagonist}'s {relationships} begin to {deteriorate}. Something ancient and hungry has followed it home.",
        ],
        kdp_keywords=["horror novel", "supernatural horror", "psychological horror", "haunted house book",
                      "gothic horror fiction", "cosmic horror", "scary book"],
        recommended_chapters=16,
        typical_price=2.99,
        generation_tip="Build dread slowly. Don't reveal the monster too early. The horror should escalate in 3 waves, with the worst saved for the final act."
    ),

    "historical": Genre(
        id="historical",
        name="Historical Fiction",
        emoji="🏛️",
        description="Stories set in vivid historical periods with real-world events as backdrop.",
        sub_genres=["WWI/WWII Fiction", "Medieval", "Victorian Era", "Ancient Rome/Greece",
                    "Renaissance", "American West", "Ancient Egypt", "Cold War"],
        premise_templates=[
            "In {year}, {location}, {protagonist} must navigate {historical_conflict} while pursuing {personal_goal}. Based around the real events of {historical_event}, this is a story of {theme} and survival.",
            "{protagonist}, a {job} in {historical_period} {location}, becomes entangled in {conflict} when {inciting_event}. As history unfolds around them, they must choose between {choice_a} and {choice_b}.",
            "The {historical_event} changed everything. {protagonist} witnessed it firsthand and carries a secret that could rewrite history. Set across {locations}, spanning {timeframe}.",
            "In the court of {ruler}, {protagonist} serves as {role}. When they discover {conspiracy}, they must navigate the deadly politics of {era} using only {skills} and {ally} as protection.",
            "Two strangers — {protagonist_a} fighting for {side_a} and {protagonist_b} caught behind {side_b}'s lines — find their fates intertwined during {historical_event}.",
        ],
        kdp_keywords=["historical fiction", "historical novel", "WWII fiction", "medieval historical",
                      "Victorian era novel", "historical romance", "war fiction"],
        recommended_chapters=20,
        typical_price=3.99,
        generation_tip="Research 5-7 specific period details (food, clothing, speech patterns) and weave them naturally. Avoid anachronistic thinking."
    ),

    "young_adult": Genre(
        id="young_adult",
        name="Young Adult",
        emoji="🌟",
        description="Coming-of-age stories for teen readers with high stakes and big emotions.",
        sub_genres=["YA Fantasy", "YA Contemporary", "YA Romance", "YA Dystopian",
                    "YA Thriller", "YA Sci-Fi", "YA Horror"],
        premise_templates=[
            "{protagonist}, 17, has always been {trait} — until {inciting_event} forces them to question everything they thought they knew about {world/self}. With {best_friend} by their side and {love_interest} complicating everything, they must {goal}.",
            "At {school/institution}, {protagonist} discovers they have {ability/power}. But using it comes at a cost: {consequence}. When {antagonist} threatens {what_they_love}, {protagonist} must decide who they want to be.",
            "The summer before {milestone} was supposed to be {expectation}. Instead, {protagonist} meets {character}, uncovers {secret}, and realizes {revelation} that changes their understanding of {theme}.",
            "Everyone in {dystopian_society} is assigned a {role/number/label} at {age}. {protagonist} refuses to accept theirs. The rebellion starts with {small_act} and ends with {climax}.",
            "{protagonist} moves to {new_place} after {life_change} and must reinvent themselves. But {complication} and an unexpected connection with {character} make starting over harder—and more important—than imagined.",
        ],
        kdp_keywords=["young adult fiction", "YA novel", "teen fiction", "coming of age book",
                      "YA fantasy", "YA romance", "young adult thriller"],
        recommended_chapters=18,
        typical_price=2.99,
        generation_tip="Voice is everything in YA. First-person present tense works well. Include friendship dynamics alongside the main plot."
    ),

    "literary": Genre(
        id="literary",
        name="Literary Fiction",
        emoji="📚",
        description="Character-driven stories exploring the human condition with artistic prose.",
        sub_genres=["Contemporary Literary", "Magical Realism", "Southern Gothic",
                    "Immigrant Fiction", "Family Saga", "Philosophical Fiction"],
        premise_templates=[
            "{protagonist}, a {age}-year-old {background}, returns to {hometown} after {years} years to {reason}. What they find forces a reckoning with {theme} and the family secrets that shaped who they became.",
            "Three generations of the {family} family, each shaped by {historical_force}. Through {protagonist}'s eyes, a portrait of {theme} in {setting} across {timespan}.",
            "In a {setting} where {magical_element} bleeds into everyday life, {protagonist} navigates {situation}. A meditation on {theme_a} and {theme_b}.",
            "{protagonist} has spent {years} years {pursuit}. When {inciting_event} forces them to stop, they must confront {internal_conflict} — a quiet, devastating story about {theme}.",
            "Two voices, {years} years apart: {protagonist_a} in {year_a} making a choice that echoes into {protagonist_b}'s {year_b} present. A novel about {theme} and the weight of the past.",
        ],
        kdp_keywords=["literary fiction", "contemporary fiction", "family saga novel", "character driven fiction",
                      "magical realism", "debut literary novel", "book club fiction"],
        recommended_chapters=15,
        typical_price=4.99,
        generation_tip="Focus on interiority and sensory detail. Each scene should do double duty: advance plot AND reveal character."
    ),

    "crime": Genre(
        id="crime",
        name="Crime Fiction",
        emoji="🔫",
        description="Heists, gangsters, crime investigations and the criminal underworld.",
        sub_genres=["Heist", "Noir", "Organized Crime", "True Crime Style",
                    "Cat and Mouse", "Crime Caper", "White Collar Crime"],
        premise_templates=[
            "{protagonist}, {background}, is offered one last job: {heist_target} worth {amount}. With a crew of {number} specialists, each with their own agenda, they have {timeframe} to plan the perfect crime — not knowing that {complication}.",
            "When {protagonist}'s {relationship} is killed by {criminal_faction}, they have two choices: run or go to war. A gritty crime novel set in {city}'s underworld, where {protagonist} must become the thing they feared.",
            "{protagonist} has walked both sides of the law. Now working as {job}, they're hired to {task} that leads straight back into the {criminal_world} they escaped. The only person they can trust is {ally} — and even that's uncertain.",
            "The {amount} heist was flawless. Then {complication} and now {protagonist} is the only member of the crew not in handcuffs — or a body bag. They have {timeframe} to figure out who betrayed them.",
            "White-collar {job} {protagonist} discovers that {corporation} has been {crime} for {years}. Blowing the whistle means {consequence}. Staying silent means {other_consequence}. A crime thriller about moral compromise.",
        ],
        kdp_keywords=["crime fiction", "heist novel", "noir fiction", "crime thriller",
                      "organized crime novel", "crime caper", "gangster fiction"],
        recommended_chapters=18,
        typical_price=3.99,
        generation_tip="Establish the rules of your criminal world early. Every plan should go wrong in at least one unexpected way."
    ),

    "self_help": Genre(
        id="self_help",
        name="Self-Help / Non-Fiction",
        emoji="💪",
        description="Practical guides, productivity, mindset, and personal transformation.",
        sub_genres=["Productivity", "Mindset", "Relationships", "Finance",
                    "Health & Wellness", "Career", "Spirituality", "Parenting"],
        premise_templates=[
            "The {number}-{unit} method that helped {author_background} go from {before_state} to {after_state}. A practical guide to {goal} using {framework} — without {common_misconception}.",
            "Why everything you've been told about {topic} is wrong — and the {evidence_based} approach that actually works. Based on {research/experience}, this book reveals {core_insight}.",
            "The hidden reason you {common_struggle}: it's not {common_excuse}, it's {real_cause}. A step-by-step system to {transformation} in {timeframe}.",
            "{number} principles from {field} applied to {life_area}. How {author_background} used these to {achievement} and how you can replicate the results starting {timeframe}.",
            "Stop {negative_behavior}. Start {positive_behavior}. The science of {topic} explained simply, with {number} actionable exercises that create lasting change.",
        ],
        kdp_keywords=["self help book", "personal development", "productivity book", "mindset book",
                      "self improvement", "motivational book", "life changing book"],
        recommended_chapters=12,
        typical_price=4.99,
        generation_tip="Each chapter should have: a concept, a story illustrating it, research backing it, and 1-3 actionable exercises."
    ),

    "business": Genre(
        id="business",
        name="Business & Finance",
        emoji="💼",
        description="Entrepreneurship, investing, leadership, and money strategies.",
        sub_genres=["Entrepreneurship", "Investing", "Marketing", "Leadership",
                    "Startup Culture", "Passive Income", "Crypto/Web3", "Real Estate"],
        premise_templates=[
            "How {author_background} built a {revenue}-per-{period} {business_type} from scratch with {starting_capital} and no {common_advantage}. The exact {number}-step system, including the {number} mistakes that nearly killed it.",
            "The {investing_strategy} strategy that {achievement} — explained in plain language without {jargon}. Why {conventional_wisdom} is costing you {cost} and what to do instead.",
            "A {job_title}'s guide to {goal}: the frameworks, scripts, and systems used by {company_type} to {achievement}. Works for {audience} at any stage.",
            "What {successful_people} know about {topic} that nobody teaches you. {number} unconventional principles for {outcome}, with case studies from {industry}.",
            "The {number}-year roadmap to {financial_goal}. Not theory — a detailed plan with {specific_strategies}, tax considerations, and risk management for {audience}.",
        ],
        kdp_keywords=["business book", "entrepreneurship book", "investing guide", "passive income book",
                      "startup book", "financial freedom book", "make money online"],
        recommended_chapters=12,
        typical_price=4.99,
        generation_tip="Lead with the promise, deliver with specifics. Include real numbers and examples. End every chapter with a quick-win action step."
    ),

    "paranormal": Genre(
        id="paranormal",
        name="Paranormal",
        emoji="🌙",
        description="Vampires, werewolves, witches, fae, and other supernatural beings.",
        sub_genres=["Vampire Romance", "Werewolf Romance", "Witch Fiction", "Fae/Fey",
                    "Angel/Demon", "Shifter Romance", "Necromancer", "Ghost Stories"],
        premise_templates=[
            "{protagonist}, a {human_job}, never believed in {supernatural_type} — until one saved her life in {location}. Now bound by {magical_rule} to {love_interest}, a {species} who is everything she shouldn't want.",
            "The {species} world has been secret for {years} centuries. When {protagonist} accidentally witnesses {event}, {love_interest} has two choices: {option_a} or {option_b}. Neither is simple when {complication}.",
            "{protagonist} wakes on their {age}th birthday with {power}. Welcome to the {supernatural_community} — a world of {faction_a}, {faction_b}, and ancient laws that {protagonist} is already breaking.",
            "In a world where {supernatural_type} and humans coexist (barely), {protagonist} is the {rare_status} who belongs to neither world. When {inciting_event}, they become the key to {conflict_resolution}.",
            "The {object/place} has been {protagonist}'s family's {significance} for generations. When {love_interest} appears to claim it, {protagonist} discovers their bloodline carries a {secret} that changes everything.",
        ],
        kdp_keywords=["paranormal romance", "vampire romance book", "werewolf shifter romance",
                      "witch fiction", "fae romance", "supernatural romance", "paranormal fiction"],
        recommended_chapters=20,
        typical_price=2.99,
        generation_tip="Establish the supernatural rules clearly but leave room for exceptions. The romance arc should mirror the supernatural conflict."
    ),

    "western": Genre(
        id="western",
        name="Western",
        emoji="🤠",
        description="Frontier justice, outlaws, ranchers, and the American West.",
        sub_genres=["Classic Western", "Western Romance", "Weird West", "Neo-Western",
                    "Outlaw Western", "Western Mystery"],
        premise_templates=[
            "{protagonist}, a {background} with a past, rides into {town} looking for {goal}. What they find is a town under the thumb of {antagonist} and a conflict that forces them to choose between {choice_a} and {choice_b}.",
            "The {year} land rush brought fortune-seekers to {territory}. {protagonist} came for {reason} and found {complication}. A story of {theme} in a land where law is whatever the fastest gun says it is.",
            "Outlaw {protagonist} has one last job before going straight: {heist}. But {complication} and an unexpected {character} make retiring a lot harder than planned.",
            "{protagonist}, a {role} in {territory}, investigates a string of {crimes} that locals blame on {scapegoat}. The truth leads to {revelation} and a showdown that will determine who controls {territory}.",
            "Two people, one {contested_resource}: {protagonist_a}, who inherited the {resource}, and {protagonist_b}, who was promised it. A story set across {timeframe} in the American West, about {theme}.",
        ],
        kdp_keywords=["western novel", "western fiction", "cowboy romance", "frontier fiction",
                      "outlaw western", "western adventure", "classic western book"],
        recommended_chapters=15,
        typical_price=2.99,
        generation_tip="Landscape is a character in westerns. Describe the heat, dust, and isolation. Dialogue should be sparse and meaningful."
    ),

    "adventure": Genre(
        id="adventure",
        name="Adventure",
        emoji="🧭",
        description="Action-packed journeys, exploration, and high-octane quests.",
        sub_genres=["Action Adventure", "Survival", "Treasure Hunt", "Jungle/Sea Adventure",
                    "Military Adventure", "Exploration"],
        premise_templates=[
            "{protagonist}, a {background}, is hired to {mission} in {dangerous_location}. What starts as {expectation} becomes a fight for survival against {obstacles} with {companions} and a {secret} that changes everything.",
            "A {number}-year-old map leads {protagonist} to believe the legendary {artifact/place} is real. With {antagonist} and {faction} racing to find it first, the expedition becomes a deadly chase across {locations}.",
            "When {disaster} strikes {location}, {protagonist} and {group} are cut off from {safety}. With {resources} and {timeframe}, they must traverse {terrain} to reach {goal}.",
            "Mercenary {protagonist} takes a job protecting {cargo} from {city} to {destination}. Three days, {obstacles}, and a growing suspicion that the real target is {revelation}.",
            "{protagonist} survives a {disaster} that kills {number} others. Stranded in {location} with {limited_resources}, they discover {secret_about_location} that changes the stakes from survival to something much larger.",
        ],
        kdp_keywords=["adventure novel", "action adventure book", "survival fiction", "treasure hunt novel",
                      "action thriller", "adventure series", "fast paced adventure"],
        recommended_chapters=18,
        typical_price=3.99,
        generation_tip="Every 3 chapters, raise the physical stakes. The protagonist should solve problems with ingenuity, not luck."
    ),

    "childrens": Genre(
        id="childrens",
        name="Children's Fiction",
        emoji="🧸",
        description="Stories for young readers ages 6-12 with wonder, friendship, and adventure.",
        sub_genres=["Middle Grade Fantasy", "Middle Grade Adventure", "Chapter Books",
                    "School Stories", "Animal Stories", "Funny/Humorous"],
        premise_templates=[
            "{protagonist}, {age}, discovers {magical_object/ability} in {location}. Together with {best_friend} and {animal_companion}, they must {goal} before {deadline}. A story about {theme} for readers aged {age_range}.",
            "The new kid at {school} has a secret: {secret}. When {inciting_event} threatens the school, {protagonist} must use their {skill} to save the day — and make their first real friends in the process.",
            "{protagonist} finds a {creature/portal/map} that leads to {hidden_world}. But getting back home means solving {puzzle} — and maybe changing {world} for the better along the way.",
            "Every kid on {street/town} knows the legend of {legend}. Nobody believed it was real — until {protagonist} found {proof}. A funny, heartfelt adventure about {theme}.",
            "{protagonist} just wants {simple_goal}. Instead, they get {chaos}. A hilarious middle-grade adventure involving {elements}, with a message about {theme}.",
        ],
        kdp_keywords=["children's fiction", "middle grade novel", "kids adventure book",
                      "middle grade fantasy", "chapter book series", "funny kids book", "ages 8-12 fiction"],
        recommended_chapters=14,
        typical_price=2.99,
        generation_tip="Keep chapters short (1500-2000 words). Use humor, action, and dialogue-heavy scenes. The protagonist must solve the problem, not adults."
    ),

    "memoir": Genre(
        id="memoir",
        name="Memoir / Biography",
        emoji="📓",
        description="True-life stories, personal journeys, and inspirational biographies.",
        sub_genres=["Personal Memoir", "Celebrity Biography", "Trauma & Recovery",
                    "Travel Memoir", "Professional Journey", "Family History"],
        premise_templates=[
            "The story of how {protagonist} went from {starting_point} to {ending_point} — and what {years} years of {journey} taught them about {theme}. Honest, raw, and ultimately hopeful.",
            "When {protagonist} was diagnosed with / experienced {challenge}, they were told {limiting_belief}. This is the story of how they {overcame} — and the unlikely {sources_of_strength} that got them there.",
            "From {origin} to {destination}: {protagonist}'s {timeframe} journey through {landscape/industry/experience}. A memoir about {theme_a}, {theme_b}, and finding {what_they_found}.",
            "Nobody expected {protagonist} to {achievement}. This is the true story of {background}, {obstacle}, and the {turning_point} that changed everything.",
            "Part travel memoir, part personal reckoning: {protagonist}'s {timeframe} in {location} forced them to confront {internal_struggle} and rediscover {what_they_found}.",
        ],
        kdp_keywords=["memoir", "biography book", "inspirational memoir", "true story book",
                      "personal story nonfiction", "recovery memoir", "travel memoir"],
        recommended_chapters=15,
        typical_price=4.99,
        generation_tip="Open in a high-stakes moment, then step back to tell the full story. End with reflection on what the experience meant."
    ),

    "erotica": Genre(
        id="erotica",
        name="Erotica / Steamy Romance",
        emoji="🔥",
        description="Explicit adult romance with high emotional and physical stakes.",
        sub_genres=["Contemporary Erotica", "Historical Erotica", "BDSM", "Reverse Harem",
                    "Steamy Paranormal", "Dark Romance", "Forbidden Romance"],
        premise_templates=[
            "{protagonist_f} never planned on {situation} with {protagonist_m}, the {description} who {role_in_her_life}. When {circumstances} throw them together, what starts as {initial_dynamic} becomes {emotional_depth} wrapped in {heat_level} passion.",
            "Forbidden by {rule/circumstance}, {protagonist_a} and {protagonist_b} shouldn't want each other. They absolutely do. A steamy, emotionally-charged story about {theme} with a guaranteed {ending}.",
            "One night was supposed to be enough. Then {complication}. Now {protagonist} can't stay away from {love_interest} — even though {reason_they_should}. A dark romance about {theme}.",
            "{protagonist} inherits a {business/object/role} and along with it, an obligation to {love_interest}. What follows is {timeframe} of tension, desire, and secrets that change everything.",
            "Rules: {rule_1}. {rule_2}. No feelings. {protagonist} breaks all three within {timeframe}. A steamy reverse harem / contemporary romance with {heat_level} scenes and a {ending_type} ending.",
        ],
        kdp_keywords=["steamy romance", "adult romance novel", "dark romance book", "forbidden romance",
                      "reverse harem romance", "spicy romance", "18+ romance novel"],
        recommended_chapters=18,
        typical_price=2.99,
        generation_tip="Emotional tension must match physical tension. Each intimate scene should reveal something new about character or relationship dynamics."
    ),

    "spiritual": Genre(
        id="spiritual",
        name="Spiritual / Inspirational",
        emoji="🚩",
        description="Faith journeys, spiritual transformation, and finding meaning.",
        sub_genres=["Christian Fiction", "Inspirational Non-Fiction", "Mindfulness",
                    "New Age", "Buddhist Fiction", "Faith Journey"],
        premise_templates=[
            "After {crisis_event}, {protagonist} loses their faith in {what_they_believed}. A journey across {setting} — and inward — toward a {theme} they never expected to find.",
            "{protagonist} has always followed {rules/tradition}. When {inciting_event} challenges everything, they must choose between {old_way} and {new_understanding}. An inspirational story about {theme}.",
            "The {spiritual_practice} {protagonist} stumbled into by accident changed everything. This is how {timeframe} of {journey} revealed {core_truth} — and what you can take from it.",
            "In {setting}, {protagonist} encounters {spiritual_figure/event} that sets them on a path they can't explain and can't ignore. A novel of {theme} and the search for {what_they_seek}.",
            "When the {title/role} of {spiritual_community} passes to {protagonist}, they're the last person anyone expected — including themselves. A story about {theme}, {theme_2}, and what it means to lead.",
        ],
        kdp_keywords=["inspirational fiction", "Christian novel", "spiritual memoir", "faith based fiction",
                      "inspirational story", "feel good spiritual book", "mindfulness fiction"],
        recommended_chapters=14,
        typical_price=3.99,
        generation_tip="Ground abstract spiritual concepts in concrete sensory scenes. The protagonist's internal transformation should be visible through their actions."
    ),
}


def get_all_genres() -> list[Genre]:
    return list(GENRES.values())


def get_genre(genre_id: str) -> Optional[Genre]:
    return GENRES.get(genre_id)


def get_random_premise(genre_id: str, fill_placeholders: bool = False) -> str:
    """Return a random premise template for the given genre.
    If fill_placeholders=True, replaces {placeholders} with generic defaults."""
    genre = get_genre(genre_id)
    if not genre:
        raise ValueError(f"Unknown genre: {genre_id}")
    template = random.choice(genre.premise_templates)
    if fill_placeholders:
        import re
        placeholders = re.findall(r"\{([^}]+)\}", template)
        for ph in placeholders:
            defaults = {
                "protagonist": "Alex Carter",
                "protagonist_f": "Emma Hayes",
                "protagonist_m": "Liam Cross",
                "love_interest": "Jordan",
                "antagonist": "a shadowy organization",
                "setting": "a city on the edge of collapse",
                "location": "an abandoned warehouse district",
                "city": "New York",
                "year": "2031",
                "age": "32",
                "timeframe": "72 hours",
                "deadline": "midnight",
                "goal": "uncover the truth",
                "theme": "identity and survival",
                "job": "former detective",
                "background": "ex-military operative",
            }
            replacement = defaults.get(ph, ph.replace("_", " ").title())
            template = template.replace("{" + ph + "}", replacement, 1)
    return template


def build_full_premise(genre_id: str, custom_fields: dict[str, str]) -> str:
    """Build a premise from a template, filling provided fields and leaving others as hints."""
    genre = get_genre(genre_id)
    if not genre:
        raise ValueError(f"Unknown genre: {genre_id}")
    template = random.choice(genre.premise_templates)
    for key, value in custom_fields.items():
        template = template.replace("{" + key + "}", value)
    return template


if __name__ == "__main__":
    import json
    print(f"Available genres: {len(GENRES)}")
    for g in get_all_genres():
        print(f"  {g.emoji} {g.name} ({g.id}) — {g.recommended_chapters} chapters @ ${g.typical_price}")
    print("\nSample thriller premise:")
    print(get_random_premise("thriller", fill_placeholders=True))
