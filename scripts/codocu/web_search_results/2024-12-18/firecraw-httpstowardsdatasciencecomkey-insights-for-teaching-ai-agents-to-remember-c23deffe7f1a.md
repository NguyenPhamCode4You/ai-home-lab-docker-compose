

📖 **Crawling content from https://towardsdatascience.com/key-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a**...

[Open in app](https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2Fc23deffe7f1a&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderCollection&source=---top_nav_layout_nav----------------------------------)

[Sign up](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=post_page---top_nav_layout_nav-----------------------global_nav-----------)

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=post_page---top_nav_layout_nav-----------------------global_nav-----------)

[Homepage](https://medium.com/?source=---top_nav_layout_nav----------------------------------)

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav-----------)

[Sign up](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=post_page---top_nav_layout_nav-----------------------global_nav-----------)

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=post_page---top_nav_layout_nav-----------------------global_nav-----------)

![](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

# Key Insights for Teaching AI Agents to Remember

## Recommendations on building robust memory capabilities based on experimentation with Autogen’s “Teachable Agents”

[![Sandi Besen](https://miro.medium.com/v2/resize:fill:88:88/1*gHEvwZHf-nDi0QXwnsUeFg.jpeg)](https://medium.com/@sandibesen?source=post_page---byline--c23deffe7f1a--------------------------------)

[![Towards Data Science](https://miro.medium.com/v2/resize:fill:48:48/1*CJe3891yB1A1mzMdqemkdg.jpeg)](https://towardsdatascience.com/?source=post_page---byline--c23deffe7f1a--------------------------------)

[Sandi Besen](https://medium.com/@sandibesen?source=post_page---byline--c23deffe7f1a--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F23260bfdf2e&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&user=Sandi+Besen&userId=23260bfdf2e&source=post_page-23260bfdf2e--byline--c23deffe7f1a---------------------post_header-----------)

Published in

[Towards Data Science](https://towardsdatascience.com/?source=post_page---byline--c23deffe7f1a--------------------------------)

·

16 min read

·

Sep 9, 2024

150

2

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dc23deffe7f1a&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=---header_actions--c23deffe7f1a---------------------post_audio_button-----------)

Share

Memory is undoubtedly becoming a crucial aspect of Agentic AI. As the use cases for AI Agents grow in complexity, so does the need for these agents to learn from past experiences, utilize stored business-specific knowledge, and adapt to evolving scenarios based on accumulated information.

In my previous article, “ [Memory in AI: Key Benefits and Investment Considerations](https://medium.com/towards-data-science/the-important-role-of-memory-in-agentic-ai-896b22542b3e),” I explored why memory is pivotal for AI, discussing its role in recall, reasoning, and continuous learning. This piece, however, will dive directly into the implementation of memory by examining its impact through the “teachability” functionality in the popular agent framework, [Autogen](https://microsoft.github.io/autogen/).

**_Note_** _:_ _While this article is technical in nature, it offers value for both technical professionals and business leaders looking to evaluate the role of memory in Agentic AI systems. I’ve structured it so that readers can skip over the code sections and still grasp the way memory can augment the responses of your AI systems. If you don’t wish to follow the code, you may read the descriptions of each step to get a sense of the process… or just the key findings and recommendations section._

![](https://miro.medium.com/v2/resize:fit:700/1*0r3eOl-ipZGcaTHBXEMBcw.jpeg)

Source: Dalle3 , Prompt Author:Sandi Besen

# Key Findings and Recommendations

My exploration of Autogen’s Teachable Agents revealed both their potential and limitations in handling both simple and complex memory tasks.

Out of the box, Autogen’s TeachableAgent performs less brilliantly than expected. The Agen’ts reasoning ability conflates memories together in a non productive way and the included retrieval mechanism is not set up for multi-step searches necessary for answering complex questions. **This limitation suggests that if you would like to use Autogen’s Teachable Agents, there needs to be substantial customization to both supplement reasoning capabilities and achieve more sophisticated memory retrieval.**

**To build more robust memory capabilities, it’s crucial to implement multi-step search functionality.** A single memory search often falls short of providing the comprehensive information needed for complex tasks. Implementing a series of interconnected searches could significantly enhance the agent’s ability to gather and synthesize relevant information.

**The “teachability” feature, while powerful, should be approached with caution**. **Continuous activation without oversight risks data poisoning and compromise of trusted information sources**. Business leaders and solution architects should consider implementing a human-in-the-loop approach, allowing users to approve what the system learns versus treating every inference as ground truth the system should learn from. This oversight in Autogen’s current Teachable Agent design could cause significant risks associated with unchecked learning.

Lastly, the method of memory retrieval from a knowledge store plays a large role in the system’s effectiveness. **Moving beyond simple nearest neighbor searches, which is the TeachableAgent’s default, to more advanced techniques such as hybrid search** (combining keyword and vector approaches), **semantic search, or knowledge graph utilization** **could dramatically improve the relevance and accuracy of retrieved information**.

# Descriptive Code Implementation

To appropriately demonstrate how external memory can be valuable, I created a fictitious scenario for a car parts manufacturing plant. Follow the code below to implement a Teachable Agent yourself.

**_Scenario_** _: A car parts manufacturing facility needs to put a plan in place in case there are energy constraints. The plan needs to be flexible and adapt based on how much power consumption the facility can use and which parts and models are in demand._

**Step 1:**

Pre- set up requires you to pip install autogen if you don’t have it installed in your active environment and create a config JSON file.

Example of a compatible config file which uses Azure OpenAI’s service model GPT4–o:

```
[{\
    "model": "gpt-4o",\
    "api_key": "<YOUR API KEY>",\
    "azure_endpoint": "<YOUR ENDPOINT>",\
    "api_type": "azure",\
    "api_version": "2024-06-01"\
}]
```

Install Autogen for python:

```
pip install pyautogen
```

**Step 2:**

Import the necessary libraries to your notebook or file and load the config file.

```
import autogen
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent, UserProxyAgent

config_list = autogen.config_list_from_json(
    env_or_file="autogenconfig.json", #the json file name that stores the config
    file_location=".", #this means the file is in the same directory
    filter_dict={
        "model": ["gpt-4o"], #select a subset of the models in your config
    },
)
```

**Step 3:**

Create the Agents. We will need two agents because of the way that Autogen’s framework works. We use a UserProxyAgent to execute tasks and interact with or replace human involvement (depending on the desired amount of human in the loop). We also create a Conversable Agent as the “Teachable Agent” which is meant to interact with other agents (not the user). You can read more about the [UserProxyAgents](https://microsoft.github.io/autogen/docs/reference/agentchat/user_proxy_agent/) and [ConversableAgents](https://microsoft.github.io/autogen/docs/reference/agentchat/conversable_agent/) here.

```
teachable_agent = ConversableAgent(
    name="teachable_agent",  # the name can't contain spaces
    llm_config={"config_list": config_list, "timeout": 120, "cache_seed": None},  # in this example we disable caching but if it is enabled it caches API requests so that they can be reused when the same request is used
)

user = UserProxyAgent(
    name="user",
    human_input_mode="ALWAYS", #I want to have full control over the code executed so I am setting human_input_mode to ALWAYS. Other options are NEVER and TERMINATE.
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False, #setting a termination  message is VERY important because it tells the agent when to finish.
    max_consecutive_auto_reply=0, #we don't need this agent to replies multiple times in a row
    code_execution_config={
        "use_docker": False
    },  # If you are planning on running code look into setting use_docker=True. For this example I am not because then I have to walk through the docker setup, but it is safer than running the code directly.
)
```

**Step 4:**

To have a baseline, let’s ask the same question to the agents before and after we “teach” it. I purposely decided to demonstrate different levels of question difficulty to show performance on tasks that require a single step vs multistep memory retrieval. To successfully address the intricate multi-step question, the retrieval mechanism must provide information from two separate memories as context to the language model responsible for generating a final response.

**Simple Question**: “The facility is experiencing a power shortage of 40%. What models need to be prioritized?”

**Complex Multi Step Question**: “The facility is experiencing a power shortage of 40%. Provide me a detailed breakdown of what machines should be deactivated and which machines should remain active.”

As expected the responses are generic and not particularly applicable to an individual business.

**Response prior to enabling long term memory:**

```
SIMPLE QUESTION RESPONSE
===========================
>>>>>>>> USING AUTO REPLY...
teachable_agent (to user):

To address a power shortage of 30% effectively, it's crucial to prioritize models that are essential to critical operations, safety, and those that have the highest impact on productivity. Here are steps to determine which models to prioritize:

1. **Identify Essential Systems:** Prioritize systems that are vital for safety, security, and essential operations. These might include:
   - Emergency lighting
   - Security systems (alarms, surveillance)
   - Critical environmental controls (e.g., refrigeration for hazardous materials)
   - Communication systems

2. **Evaluate Impact on Core Operations:** Determine which models are crucial to the facility’s core functions. This can include machinery, servers, or any processes that are indispensable for maintaining productivity and operations.

3. **Energy Efficiency:** Prioritize models and equipment that are more energy-efficient and can operate within the reduced power capacity.

4. **Downtime Cost:** Consider the cost of downtime for each model. Prioritize those where downtime would result in significant financial losses or production delays.

Based on these principles, here’s a generic prioritization framework:

1. **Safety and Security Systems:**
   - Emergency Lighting
   - Fire Alarms and Sprinkler Systems
   - Security Cameras and Sensors

2. **Critical Operational Systems:**
   - Essential Production Machinery (that cannot be shut down without major issues)
   - Servers and IT Infrastructure (especially those critical for operations and data integrity)
   - HVAC Systems (if necessary for maintaining safe operating conditions)

3. **Support Systems:**
   - Backup Power Systems (uninterruptible power supplies, generators)
   - Communication Systems (both internal and external communication)

Ensure that non-essential and high energy-consuming equipment is powered down or scheduled to operate during off-peak hours if possible.

Always re-evaluate periodically to ensure that the power allocation aligns with the dynamic needs of the facility. Communication with key stakeholders regarding priorities and decisions is also essential for smooth operations during a power shortage.

COMPLEX MULTISTEP QUESTION RESPONSE
====================================
>>>>>>>> USING AUTO REPLY...
teachable_agent (to user):

To effectively manage a facility experiencing a 30% power shortage, we need to prioritize essential operations and consider the criticality and energy consumption of each machine. Here is a detailed breakdown:

### Step 1: Identify Essential Operations

1. **Critical Infrastructure**: Safety systems, security systems, and essential IT infrastructure.
2. **Production Lines**: Machines involved in the primary production process.
3. **Support Systems**: HVAC systems, lighting, and other ancillary equipment necessary to maintain a safe working environment.

### Step 2: Categorize Machines by Importance and Energy Consumption

#### A. Essential and High-Energy Machines

1. **Safety and Security Systems**
   - Fire alarms and sprinklers
   - Surveillance cameras
   - Security access controls

2. **Primary Production Machines**
   - Core production lines
   - Central processing units or mainframe servers (for IT-heavy operations)

3. **Critical Support Systems**
   - Emergency lighting
   - Essential HVAC systems (for maintaining operation-critical temperature and humidity)

#### B. Non-Essential and High-Energy Machines

1. **Secondary Production Lines**
   - Non-primary or non-critical production lines
   - Equipment used for non-essential or ancillary processes

2. **Supplementary IT Infrastructure**
   - Servers used for non-essential operations
   - Backup systems that are not in immediate use

3. **Non-Essential HVAC and Lighting**
   - HVAC systems for non-critical areas
   - Lighting in non-essential zones

#### C. Non-Essential and Low-Energy Machines

1. **Office Equipment**
   - Computers, printers, and copiers in non-essential offices
2. **Non-essential Lab or Research Equipment**
   - Devices not directly linked to current essential tasks

### Step 3: Prioritize Deactivation

#### Immediate Deactivation

1. **Non-Essential and High-Energy Machines**
   - Secondary production lines
   - Non-essential backup servers

2. **Non-Essential HVAC and Lighting**
   - HVAC in non-critical areas
   - Non-essential lighting

3. **Non-Essential Office Equipment**
   - Printers, non-essential computers, and copiers

#### Limited Usage

1. **Essential and High-Energy Machines**
   - Operate critical production lines at reduced capacity if possible
   - Implement rotational operation schedules for essential processes

2. **Critical Support Systems**
   - Optimize HVAC settings (e.g., raising or lowering set points within acceptable ranges)
   - Reduce lighting to minimum safety standards

### Step 4: Implement Energy Conservation Measures

1. **Optimize Operations**
   - Utilize energy-efficient settings
   - Implement energy-saving protocols and encourage staff to conserve energy

2. **Scheduled Downtime**
   - Plan for downtime during off-peak hours for essential machinery to balance the load

3. **Regular Monitoring**
   - Monitor energy consumption in real-time to make quick adjustments as needed

### Summary

#### Remain Active:
1. Safety and security systems
2. Main production lines
3. Critical IT infrastructure
4. Essential HVAC and lighting for operational areas

#### Deactivate or Limit Use:
1. Non-essential production lines
2. Redundant IT systems
3. Non-critical HVAC and lighting
4. Office equipment in non-essential areas

**Note**: These recommendations should be adjusted based on the specific operational requirements of your facility. Additionally, it could be beneficial to communicate these changes to all staff to ensure compliance and understanding.
```

Code to ask baseline questions:

```

#simple question
user.initiate_chat(teachable_agent, message="The facility is experiencing a power shortage of 40%. What models need to be prioritized?", clear_history=True)
#multistep complex question
user.initiate_chat(teachable_agent, message="The facility is experiencing a power shortage of 30%. Provide me a detailed breakdown of what machines should be deactivated and which machines should remain active.", clear_history=True)
```

**Step 5:**

Create the “teachability” capability that you then add to the agent. The Teachability class inherits from the AgentCapabiliy class, which essentially allows you to add customizable capabilities to the Agents.

The Teachability class has many optional parameters that can be further explored [here](https://github.com/microsoft/autogen/blob/main/notebook/agentchat_teachability.ipynb).

The out of the box Teachability class is a quick and convenient way of adding long term memory to the agents, but will likely need to be customized for use in a production setting, as outlined in the key findings section. It involves sending messages to an Analyzer Agent that evaluates the user messages for potential storage and retrieval. The Analyzer Agent looks for advice that could be applicable to similar tasks in the future and then summarizes and stores task-advice pairs in a binary database serving as the agent’s “memory”.

```
teachability = Teachability(
    verbosity=0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
    reset_db=True, # we want to reset the db because we are creating a new agent so we don't want any existing memories. If we wanted to use an existing memory store we would set this to false.
    path_to_db_dir="./tmp/notebook/teachability_db", #this is the default path you can use any path you'd like
    recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
    max_num_retrievals=10 #10 is default bu you can set the max number of memos to be retrieved lower or higher
)

teachability.add_to_agent(teachable_agent)
```

**Step 6:**

Now that the teachable\_agent is configured, we need to provide it the information that we want the agent to “learn” (store in the database and retrieve from).

In line with our scenario, I wanted the agent to have basic understanding of the facility which consisted of:

- the types of components the manufacturing plant produces
- the types of car models the components need to be made for
- which machines are used to make each component

Additionally, I wanted to provide some operational guidance on the priorities of the facility depending on how power constrained it is. This includes:

- Guidance in case of energy capacity constraint of more than 50%
- Guidance in case of energy capacity constraint between 25–50%
- Guidance in case of energy capacity constraint between 0–25%

```
business_info = """
# This manufacturing plant manufactures the following vehicle parts:
- Body panels (doors, hoods, fenders, etc.)
- Engine components (pistons, crankshafts, camshafts)
- Transmission parts
- Suspension components (springs, shock absorbers)
- Brake system parts (rotors, calipers, pads)

# This manufactoring plant produces parts for the following models:
- Ford F-150
- Ford Focus
- Ford Explorer
- Ford Mustang
- Ford Escape
- Ford Edge
- Ford Ranger

# Equipment for Specific Automotive Parts and Their Uses

## 1. Body Panels (doors, hoods, fenders, etc.)
- Stamping presses: Form sheet metal into body panel shapes
- Die sets: Used with stamping presses to create specific panel shapes
- Hydraulic presses: Shape and form metal panels with high pressure
- Robotic welding systems: Automate welding of body panels and structures
- Laser cutting machines: Precisely cut sheet metal for panels
- Sheet metal forming machines: Shape flat sheets into curved or complex forms
- Hemming machines: Fold and crimp edges of panels for strength and safety
- Metal finishing equipment (grinders, sanders): Smooth surfaces and remove imperfections
- Paint booths and spraying systems: Apply paint and protective coatings
- Drying ovens: Cure paint and coatings
- Quality control inspection systems: Check for defects and ensure dimensional accuracy

## 2. Engine Components (pistons, crankshafts, camshafts)
- CNC machining centers: Mill and drill complex engine parts
- CNC lathes: Create cylindrical parts like pistons and camshafts
- Boring machines: Enlarge and finish cylindrical holes in engine blocks
- Honing machines: Create a fine surface finish on cylinder bores
- Grinding machines: Achieve precise dimensions and smooth surfaces
- EDM equipment: Create complex shapes in hardened materials
- Forging presses: Shape metal for crankshafts and connecting rods
- Die casting machines: Produce engine blocks and cylinder heads
- Heat treatment furnaces: Alter material properties for strength and durability
- Quenching systems: Rapidly cool parts after heat treatment
- Balancing machines: Ensure rotating parts are perfectly balanced
- Coordinate Measuring Machines (CMMs): Verify dimensional accuracy

## 3. Transmission Parts
- Gear cutting machines: Create precise gear teeth on transmission components
- CNC machining centers: Mill and drill complex transmission housings and parts
- CNC lathes: Produce shafts and other cylindrical components
- Broaching machines: Create internal splines and keyways
- Heat treatment equipment: Harden gears and other components
- Precision grinding machines: Achieve extremely tight tolerances on gear surfaces
- Honing machines: Finish internal bores in transmission housings
- Gear measurement systems: Verify gear geometry and quality
- Assembly lines with robotic systems: Put together transmission components
- Test benches: Evaluate completed transmissions for performance and quality

## 4. Suspension Components (springs, shock absorbers)
- Coil spring winding machines: Produce coil springs to exact specifications
- Leaf spring forming equipment: Shape and form leaf springs
- Heat treatment furnaces: Strengthen springs and other components
- Shot peening equipment: Increase fatigue strength of springs
- CNC machining centers: Create precision parts for shock absorbers
- Hydraulic cylinder assembly equipment: Assemble shock absorber components
- Gas charging stations: Fill shock absorbers with pressurized gas
- Spring testing machines: Verify spring rates and performance
- Durability test rigs: Simulate real-world conditions to test longevity

## 5. Brake System Parts (rotors, calipers, pads)
- High-precision CNC lathes: Machine brake rotors to exact specifications
- Grinding machines: Finish rotor surfaces for smoothness
- Die casting machines: Produce caliper bodies
- CNC machining centers: Mill and drill calipers for precise fit
- Precision boring machines: Create accurate cylinder bores in calipers
- Hydraulic press: Compress and form brake pad materials
- Powder coating systems: Apply protective finishes to calipers
- Assembly lines with robotic systems: Put together brake components
- Brake dynamometers: Test brake system performance and durability

"""

business_rules_over50 = """
- The engine components are critical and machinery should be kept online that corresponds to producing these components when capacity constraint is more or equal to 50%: engine components
- Components for the following models should be prioritized when capacity constraint is more or equal to 50%: 1.Ford F-150
"""

business_rules_25to50 = """
- The following components are critical and machinery should be kept online that corresponds to producing these components when capacity constraint is between 25-50%: engine components and transmission parts
- Components for the following models should be prioritized when capacity constraint is between 25-50%: 1.Ford F-150 2.Ford Explorer
"""

business_rules_0to25 = """
- The following components are critical and machinery should be kept online that corresponds to producing these components when capacity constraint is between 0-25%: engine components,transmission parts, Brake System Parts
- Components for the following models should be prioritized when capacity constraint is between 0-25%: 1.Ford F-150 2.Ford Explorer 3.Ford Mustang 4.Ford Focus
"""
```

```
user.initiate_chat(teachable_agent, message=business_info, clear_history=True)
```

```
user.initiate_chat(teachable_agent, message=business_rules_over50, clear_history=True)
```

```
user.initiate_chat(teachable_agent, message=business_rules_25to50, clear_history=True)
```

```
user.initiate_chat(teachable_agent, message=business_rules_0to25, clear_history=True)
```

## **Step 7:**

Now that we have added important information to long term memory, let’s ask the Agent the same question and see the difference in its responses.

**Simple Question:**“The facility is experiencing a power shortage of 40%. What models need to be prioritized?”

**Complex Multi Step Question:** “The facility is experiencing a power shortage of 40%. Provide me a detailed breakdown of what machines should be deactivated and which machines should remain active.”

**Results after implementing long term memory:**

The Teachable Agent was able to partially answer the simple question. It was correct on the car models that need to be prioritized, but it provided additional incorrect information about which components needed to be included.

The complex multi-step question was not adequately addressed. It erroneously merged two distinct business guidelines for 0–25% and 25–50% capacity constraints into a single, generalized guideline, resulting in an inaccurate response. Additionally, it only provided a partial list of machines that should remain active or be deactivated for each component’s production, omitting crucial details from the complete operational protocol. This demonstrates the challenges in accurately retrieving and synthesizing information from multiple, separate memory sources for complex queries.

```
SIMPLE QUESTION RESPONSE
===========================
>>>>>>>> USING AUTO REPLY...
teachable_agent (to user):
Given the facility is experiencing a power shortage of 40%, this falls within the 25-50% capacity constraint range. According to your previously established priorities for such a scenario, the following models and components need to be prioritized:

### Components to Prioritize
- Engine components
- Transmission parts
- Brake System Parts

### Models to Prioritize
1. Ford F-150
2. Ford Explorer

You should ensure that the machinery necessary to produce these critical components for the Ford F-150 and Ford Explorer is kept online.

COMPLEX MULTISTEP QUESTION RESPONSE
====================================
>>>>>>>> USING AUTO REPLY...
teachable_agent (to user):

In response to the 40% power shortage, let's create a detailed plan to ensure the most critical machinery remains operational while deactivating less essential ones.

### Critical Prioritization (0-50% capacity constraint):
- **Critical Components**:
  - Engine components (pistons, crankshafts, camshafts)
  - Transmission parts
  - Brake System Parts (rotors, calipers, pads)

- **Prioritized Models**:
  - Ford F-150
  - Ford Explorer

### Machines to Remain Active:
1. **Engine Component Machines**:
   - Engine Block Milling Machine
   - Crankshaft Grinding Machine
   - Camshaft Milling Machine

2. **Transmission Part Machines**:
   - Transmission Housing Caster
   - Gear Cutting Machine
   - Transmission Assembly Line

3. **Brake System Part Machines**:
   - Brake Rotor Casting Machine
   - Brake Caliper Milling Machine
   - Brake Pad Press

### Machines to Deactivate:
1. **Body Panel Machines**:
   - Door Stamping Machine
   - Hood Assembly Machine
   - Fender Bending Machine

2. **Suspension Component Machines**:
   - Coil Spring Forming Machine
   - Shock Absorber Assembly Line

### Detailed Breakdown:

#### Active Machines:
- **Engine Block Milling Machine**:
  - Produces critical engine blocks, essential for Ford F-150 and Ford Explorer.
- **Crankshaft Grinding Machine**:
  - Ensures high precision crankshafts; crucial for the performance of Ford F-150 and Ford Explorer.
- **Camshaft Milling Machine**:
  - Produces camshafts, necessary for Ford F-150 and Ford Explorer engines.

- **Transmission Housing Caster**:
  - Important for casting the housing of transmissions used in Ford F-150 and Ford Explorer.
- **Gear Cutting Machine**:
  - Precision gears production, vital for Ford F-150 and Ford Explorer transmissions.
- **Transmission Assembly Line**:
  - Assembly of complete transmission units for Ford F-150 and Ford Explorer.

- **Brake Rotor Casting Machine**:
  - Produces brake rotors, crucial for the safe braking systems in Ford F-150 and Ford Explorer.
- **Brake Caliper Milling Machine**:
  - Machining of brake calipers, essential for Ford F-150 and Ford Explorer.
- **Brake Pad Press**:
  - Manufacturing of brake pads, necessary for ensuring braking efficiency in Ford F-150 and Ford Explorer.

#### Deactivated Machines:
- **Door Stamping Machine**:
  - While important, body panels like doors are less critical than engine and transmission components under current constraints.
- **Hood Assembly Machine**:
  - Deactivating hood assembly to free up power for critical components manufacturing.
- **Fender Bending Machine**:
  - Non-critical compared to engine and brake components during a significant power shortage.
- **Coil Spring Forming Machine**:
  - Suspension springs are lower priorities under current circumstances.
- **Shock Absorber Assembly Line**:
  - Suspension components aren’t critical enough to keep operational during this level of power shortage.

This plan ensures that production focuses on maintaining the critical components needed for primary models, the Ford F-150 and Ford Explorer, thereby maximizing the utility of the remaining power while managing production constraints effectively.
```

Code:

```
#simple question
user.initiate_chat(teachable_agent, message="The facility is experiencing a power shortage of 40%. What models need to be prioritized?", clear_history=True)
#multistep complex question
user.initiate_chat(teachable_agent, message="The facility is experiencing a power shortage of 30%. Provide me a detailed breakdown of what machines should be deactivated and which machines should remain active.", clear_history=True)
```

# Conclusion

While Autogen provides a straightforward introduction to AI systems with memory, it falls short in handling complex tasks effectively.

**_When developing your own AI Agent System with memory capabilities, consider focusing on these key capabilities_** _:_

- **Implement multi-step searches** to ensure comprehensive and relevant results. This allows the agent to assess the usefulness of search outcomes and address all aspects of a query using the retrieved information. Additionally, **consider using more advanced retrieval approaches** such as semantic search, hybrid search, or knowledge graphs for the best results.
- To limit the potential for data poisoning, **develop a thoughtful approach to who should be able to “teach” the agent and when the agent should “learning”**. Based on guidelines set by the business or developer, one can also use agent reasoning to determine if something should be added to memory and by whom.
- Remove the likelihood of retrieving out of date information by **adding a memory decaying mechanism** that determines when a memory is no longer relevant or a newer memory should replace it.
- **For multi-agent systems** involving group chats or inter-agent information sharing, **explore various communication patterns**. Determine the most effective methods for transferring supplemental knowledge and establish limits to prevent information overload.

Note: The opinions expressed both in this article and paper are solely those of the authors and do not necessarily reflect the views or policies of their respective employers.

If you still have questions or think that something needs to be further clarified? Drop me a DM on [Linkedin](https://www.linkedin.com/in/sandibesen/)! I‘m always eager to engage in food for thought and iterate on my work.

![](https://miro.medium.com/v2/da:true/resize:fit:0/5c50caa54067fd622d2f0fac18392213bf92f6e2fae89b691e62bceb40885e74)

## Sign up to discover human stories that deepen your understanding of the world.

## Free

Distraction-free reading. No ads.

Organize your knowledge with lists and highlights.

Tell your story. Find your audience.

[Sign up for free](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=---post_footer_upsell--c23deffe7f1a---------------------lo_non_moc_upsell-----------)

## Membership

Read member-only stories

Support writers you read most

Earn money for your writing

Listen to audio narrations

Read offline with the Medium app

[Try for $5/month](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fplans&source=---post_footer_upsell--c23deffe7f1a---------------------lo_non_moc_upsell-----------)

[Ai Agent](https://medium.com/tag/ai-agent?source=post_page-----c23deffe7f1a--------------------------------)

[Llm](https://medium.com/tag/llm?source=post_page-----c23deffe7f1a--------------------------------)

[Artificial Intelligence](https://medium.com/tag/artificial-intelligence?source=post_page-----c23deffe7f1a--------------------------------)

[Genai](https://medium.com/tag/genai?source=post_page-----c23deffe7f1a--------------------------------)

[Hands On Tutorials](https://medium.com/tag/hands-on-tutorials?source=post_page-----c23deffe7f1a--------------------------------)

[![Towards Data Science](https://miro.medium.com/v2/resize:fill:96:96/1*CJe3891yB1A1mzMdqemkdg.jpeg)](https://towardsdatascience.com/?source=post_page---post_publication_info--c23deffe7f1a--------------------------------)

[![Towards Data Science](https://miro.medium.com/v2/resize:fill:128:128/1*CJe3891yB1A1mzMdqemkdg.jpeg)](https://towardsdatascience.com/?source=post_page---post_publication_info--c23deffe7f1a--------------------------------)

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fcollection%2Ftowards-data-science&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&collection=Towards+Data+Science&collectionId=7f60cf5620c9&source=post_page---post_publication_info--c23deffe7f1a---------------------follow_profile-----------)

[**Published in Towards Data Science**](https://towardsdatascience.com/?source=post_page---post_publication_info--c23deffe7f1a--------------------------------)

[777K Followers](/followers?source=post_page---post_publication_info--c23deffe7f1a--------------------------------)

· [Last published 15 hours ago](/the-anatomy-of-an-autonomous-agent-499b42b73124?source=post_page---post_publication_info--c23deffe7f1a--------------------------------)

Your home for data science and AI. The world’s leading publication for data science, data analytics, data engineering, machine learning, and artificial intelligence professionals.

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fcollection%2Ftowards-data-science&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&collection=Towards+Data+Science&collectionId=7f60cf5620c9&source=post_page---post_publication_info--c23deffe7f1a---------------------follow_profile-----------)

[![Sandi Besen](https://miro.medium.com/v2/resize:fill:96:96/1*gHEvwZHf-nDi0QXwnsUeFg.jpeg)](https://medium.com/@sandibesen?source=post_page---post_author_info--c23deffe7f1a--------------------------------)

[![Sandi Besen](https://miro.medium.com/v2/resize:fill:128:128/1*gHEvwZHf-nDi0QXwnsUeFg.jpeg)](https://medium.com/@sandibesen?source=post_page---post_author_info--c23deffe7f1a--------------------------------)

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F23260bfdf2e&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&user=Sandi+Besen&userId=23260bfdf2e&source=post_page-23260bfdf2e--post_author_info--c23deffe7f1a---------------------follow_profile-----------)

[**Written by Sandi Besen**](https://medium.com/@sandibesen?source=post_page---post_author_info--c23deffe7f1a--------------------------------)

[541 Followers](https://medium.com/@sandibesen/followers?source=post_page---post_author_info--c23deffe7f1a--------------------------------)

· [81 Following](https://medium.com/@sandibesen/following?source=post_page---post_author_info--c23deffe7f1a--------------------------------)

Learn along side me as I publish technical but digestible content for experts and novices alike. My opinons may not represent those of my employer.

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F23260bfdf2e&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&user=Sandi+Besen&userId=23260bfdf2e&source=post_page-23260bfdf2e--post_author_info--c23deffe7f1a---------------------follow_profile-----------)

## Responses (2)

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fkey-insights-for-teaching-ai-agents-to-remember-c23deffe7f1a&source=---post_responses--c23deffe7f1a---------------------respond_sidebar-----------)

Cancel

Respond

Respond

Also publish to my profile

![Zoya Khan](https://miro.medium.com/v2/resize:fill:32:32/1*0rOiUplKtqEmaSlPbz-ptw@2x.jpeg)

[Zoya Khan\\
\\
she/her](https://medium.com/@zoya211999?source=post_page---post_responses--c23deffe7f1a----0----------------------------)

[3 months ago](https://medium.com/@zoya211999/great-article-2df03f8ab28b?source=post_page---post_responses--c23deffe7f1a----0----------------------------)

```

Great article! Loved reading it. With so much insights in it.
I’ve also recently written an article on living a Healthy Life using AI and would love for you to check it out and share your thoughts. Looking forward to connecting and learning more from each other, feel free to follow me so we can grow together!
```

51

1 reply

Reply

![Alex Amaya](https://miro.medium.com/v2/resize:fill:32:32/1*jICy0uzwdcjmPI3VcIIR9Q.jpeg)

[Alex Amaya](https://medium.com/@grupoamaia?source=post_page---post_responses--c23deffe7f1a----1----------------------------)

[3 months ago](https://medium.com/@grupoamaia/insightful-read-loved-the-approach-to-a-real-case-scenario-ab7d634c9f68?source=post_page---post_responses--c23deffe7f1a----1----------------------------)

```

Insightful read, loved the approach to a real case scenario.
```

50

1 reply

Reply

## More from Sandi Besen and Towards Data Science

[See all from Sandi Besen](https://medium.com/@sandibesen?source=post_page---author_recirc--c23deffe7f1a--------------------------------)

[See all from Towards Data Science](https://towardsdatascience.com/?source=post_page---author_recirc--c23deffe7f1a--------------------------------)

## Recommended from Medium

## Lists

[![](https://miro.medium.com/v2/resize:fill:48:48/1*era76EGCwdY2gWSFKutuSw.jpeg)\\
\\
![](https://miro.medium.com/v2/resize:fill:48:48/1*AiTJDz5wwQFiUCf_SrBOQA.jpeg)\\
\\
![A phone with a tweet on it describing a deepfake video of the Ukrainian president, with a labeled fake image in the background](https://miro.medium.com/v2/resize:fill:48:48/1*zjPggFS8yoRtFbAP9R_3lw.jpeg)\\
\\
**AI Regulation** \\
\\
6 stories·650 saves](https://medium.com/@MediumStaff/list/ai-regulation-dfa78dfd2438?source=post_page---read_next_recirc--c23deffe7f1a--------------------------------)

[![](https://miro.medium.com/v2/resize:fill:48:48/1*w-hiT0-jA0PdwvalWi7xgw.png)\\
\\
![](https://miro.medium.com/v2/resize:fill:48:48/1*ndS9_Ae8Rw1gjesmxya1Dw.jpeg)\\
\\
![“Sakana AI revolutionizes transformer models with Neural Attention Memory Models (NAMMs), inspired by human memory. NAMMs enable transformers to selectively retain key information and forget redundancies, boosting efficiency and performance across tasks. Universally transferable, they excel in language, coding, vision, and more, without retraining. Explore smarter, faster, and more adaptable AI with our latest breakthrough in foundation model memory systems.](https://miro.medium.com/v2/resize:fill:48:48/1*l0-F7DGzG_uIYE9g-5Zxrw.jpeg)\\
\\
**Natural Language Processing** \\
\\
1860 stories·1489 saves](https://medium.com/@AMGAS14/list/natural-language-processing-0a856388a93a?source=post_page---read_next_recirc--c23deffe7f1a--------------------------------)

[![](https://miro.medium.com/v2/resize:fill:48:48/1*vzu3JPzaq2EZKTZNY9BhLA.png)\\
\\
![AI-generated image of a cute tiny robot in the backdrop of ChatGPT’s logo](https://miro.medium.com/v2/resize:fill:48:48/1*lEmL62oZdrOOWIzAAFKiFg.jpeg)\\
\\
![](https://miro.medium.com/v2/resize:fill:48:48/1*i2zLIwC9mftamP1dbciCeQ.jpeg)\\
\\
**ChatGPT** \\
\\
21 stories·915 saves](https://medium.com/@m.wasalski/list/chatgpt-3742c7a4727d?source=post_page---read_next_recirc--c23deffe7f1a--------------------------------)

[![](https://miro.medium.com/v2/da:true/resize:fill:48:48/0*M8Jq6btD0YsgaRM1)\\
\\
![](https://miro.medium.com/v2/resize:fill:48:48/1*rsp22rKwFDjiwwCcUly56Q.jpeg)\\
\\
![](https://miro.medium.com/v2/resize:fill:48:48/1*PNVLDmurJ5LoCjB9Ovdnpw.png)\\
\\
**Generative AI Recommended Reading** \\
\\
52 stories·1554 saves](https://tomsmith585.medium.com/list/generative-ai-recommended-reading-508b0743c247?source=post_page---read_next_recirc--c23deffe7f1a--------------------------------)

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--c23deffe7f1a--------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----c23deffe7f1a--------------------------------)

[Status](https://medium.statuspage.io/?source=post_page-----c23deffe7f1a--------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----c23deffe7f1a--------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----c23deffe7f1a--------------------------------)

[Press](pressinquiries@medium.com?source=post_page-----c23deffe7f1a--------------------------------)

[Blog](https://blog.medium.com/?source=post_page-----c23deffe7f1a--------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----c23deffe7f1a--------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----c23deffe7f1a--------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----c23deffe7f1a--------------------------------)

[Teams](https://medium.com/business?source=post_page-----c23deffe7f1a--------------------------------)

[iframe](https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6Le-uGgpAAAAAPprRaokM8AKthQ9KNGdoxaGUvVp&co=aHR0cHM6Ly90b3dhcmRzZGF0YXNjaWVuY2UuY29tOjQ0Mw..&hl=en&v=zIriijn3uj5Vpknvt_LnfNbF&size=invisible&cb=9iq42bs5skhb)

📖 **Summarizing content**...

The provided text is a snippet of an HTML page and does not contain information about state-of-the-art techniques to handle AI agent memory. Therefore, I cannot answer your question based on this content. 


To get information about AI agent memory techniques, I recommend searching for academic papers or articles specifically focused on that topic. You can use search engines like Google Scholar or explore online repositories like arXiv.

Some keywords that might be helpful in your search include:

* **Reinforcement learning memory**
* **Memory augmented neural networks**
* **Episodic memory in AI**
* **Long short-term memory (LSTM)**

Good luck with your research! 
