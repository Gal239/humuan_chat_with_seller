import re
import streamlit as st
import anthropic
from PIL import Image
import os
import json
import base64
from openai import OpenAI
import time
first_part="sk-proj--M2WqKiJ1jBVpJnqhztSZEHUGcPn9yYDyfC9uqzrorqBgCfPhf_Qv2Wo0900W9ko4PRr4dQdtJT3"
second_part="BlbkFJCg6mO4d69WU5n6lcEy1ftFgZW0mM327BD5"
third_part='pUhPErBVOzoJYqz2LtOyygqICb6UxYGuPRaKUfoA'

openai_client = OpenAI(api_key=first_part+second_part+third_part)
seller_data="""Fiverr Seller Profile

Name: John Knox
Username: johndoe_design
Rating: 4.8
Fiverr Status: Level Two
Location: United States
Languages Spoken:

English (Conversational)
Spanish (Native/Bilingual)
Fiverr Join Date: September 2018
Pro Seller: No
Offers Hourly Rate: No
About the Seller:
John Knox is a highly skilled graphic designer who specializes in creating visually engaging graphics that capture the essence of your brand. His graphic design services span print and digital media, as well as branding. He adopts a collaborative and client-centered approach, working closely with clients to understand their vision and translate it into outstanding design solutions. John caters to a wide range of clients, including small business owners and entrepreneurs, delivering exceptional results that help achieve their marketing and branding goals.

Key Expertise and Skills:

Graphic Design
Branding
Adobe Illustrator, Photoshop, Premiere Pro, After Effects
Social Media Design and Marketing
Logo, Flyer, Brochure, App, Banner, T-shirt, and Invitation Design
Presentation Design
Video Marketing
Spanish Translation
Creative Writing
Spokesperson and Voice Over
Education:

Tyler Junior College:
Associate Degree in Advertising and Public Relations (2016)
Associate Degree in Broadcast Journalism (2016)
Associate Degree in Graphic Design Multimedia (2017)
Associate Degree in Media Production (2017)
Palm Beach State College:
Associate Degree in Graphic Design Technology (2019)
Certifications:

Certification in Media Technology (2017)
Certification in Media Sales (2017)
1st Place in Newspaper Division 4 Spanish Writing (2016)
2nd Place in News Writing Spanish (2016)
2nd Place in TV Announcements Spanish (2017)
Gigs Offered by John Knox on Fiverr

Gig 1: Design Business Promo Brochure, Flyer, Ad, Poster, Sign, Banner
Description:
John offers standout brochures, flyers, and ads for your business. He collaborates with clients to transform ideas into visually compelling designs that reflect their brand and resonate with their audience.

Packages:

Tier 1 Package ($85): Custom-designed brochure, flyer, or ad for digital/print use.
Tier 2 Package ($125): Includes additional design elements and up to two revisions.
Tier 3 Package ($165): Comprehensive design package with source files for future editing.
Services Offered:

High-resolution files suitable for both digital and print use.
Source files provided for easy future modifications.
Branding elements like logos and style guides integrated seamlessly.
Requirements for Clients:

Specify the type of material (e.g., brochure, flyer, ad).
Provide references, logos, and branding elements.
Share goals, target audience, and campaign objectives.
Indicate text/copy, key messages, and calls to action.
Frequently Asked Questions:

What file formats are provided? High-resolution files for digital and print use, plus source files.
Can you customize designs? Yes, John offers a CUSTOM VIP SERVICE for personalized requests.
Are printing services included? No, but files will be print-ready.
Communication Style:
John emphasizes gratitude, collaboration, and professionalism. He encourages client feedback and ensures designs align with expectations.

Gig 2: Design or Redesign Interactive Websites and Landing Pages
Description:
John specializes in designing visually stunning UI layouts for websites and landing pages. While he focuses on design, he collaborates with developers to ensure smooth project execution.

Packages:

Tier 1 Package ($135): One-page design, mobile responsive, with source file.
Tier 2 Package ($375): Three pages (e.g., About, Services) with interaction and VIP service.
Tier 3 Package ($550): Five pages, full interaction, and comprehensive design solutions.
Services Offered:

UI layout design for single-page or multi-page websites.
Mobile-responsive designs with interaction.
Logo, branding, and style integration into the website.
Requirements for Clients:

Specify the type of website (single or multi-page).
Provide content, imagery, and branding elements (logos, color palettes).
Share goals and objectives for the website.
Examples of competitor or reference websites are encouraged.
Frequently Asked Questions:

Can I contact you before placing an order? Yes, John is available for pre-order discussions.
Do you handle development? No, John provides designs but can collaborate with developers.
What do you need to get started? Branding elements, a list of pages, and content for the website.
Communication Style:
John maintains a clear, professional, and friendly tone. He emphasizes understanding client needs, provides organized processes, and proactively seeks feedback.

Portfolio:
View John’s work at www.behance.net/phurtado123 to explore his previous projects and design style.

"""


def get_typing_animation_html():
    return """
        <style>
            .chat-bubble {
                background: white;
                padding: 16px 28px;
                border-radius: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                display: inline-block;
                margin: 10px;
                position: relative;
            }

            .typing {
                display: flex;
                align-items: center;
                gap: 6px;
                height: 18px;
            }

            .typing-dot {
                width: 8px;
                height: 8px;
                background: #93959f;
                border-radius: 50%;
                animation: typingAnimation 1.4s infinite;
                opacity: 0.4;
            }

            .typing-dot:nth-child(1) {
                animation-delay: 0s;
            }

            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }

            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes typingAnimation {
                0%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                50% {
                    transform: translateY(-4px);
                    opacity: 1;
                }
            }

            @media (prefers-color-scheme: dark) {
                .chat-bubble {
                    background: #3a3b3c;
                }
                .typing-dot {
                    background: #b0b3b8;
                }
            }
        </style>

        <div class="chat-bubble">
            <div class="typing">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    """


def display_message_with_animation(message, container):
    """Display a message with typing animation"""
    # Show typing animation
    typing_container = container.empty()
    typing_container.markdown(get_typing_animation_html(), unsafe_allow_html=True)
    # Sleep to show animation
    time.sleep(1.5)
    # Clear typing animation and show message
    typing_container.empty()
    container.markdown(message)



def parse_messages(content):
    """Parse message tags and return a list of message contents with tags removed"""
    # First check if there are any message tags
    pattern = r'<message \d+>(.*?)</message \d+>'
    messages = re.findall(pattern, content, re.DOTALL)

    if not messages:
        # Remove any stray tags that might exist
        cleaned_content = re.sub(r'<message \d+>|</message \d+>', '', content)
        return [cleaned_content.strip()]

    # For each message, remove any nested tags that might exist
    cleaned_messages = []
    for msg in messages:
        # Remove any nested message tags
        cleaned_msg = re.sub(r'<message \d+>|</message \d+>', '', msg)
        cleaned_messages.append(cleaned_msg.strip())

    return cleaned_messages


def ask_gpt(massage_history,model="gpt-4o-mini",max_tokens=4000,temperature=0,return_str=True,response_format={"type": "json_object"},print_tokens=True,parse_json=False,tools=None,parallel_tool_calls=None):
    if tools is not None:
        response_format = {"type": "text"}
        parallel_tool_calls=False
        response = openai_client.chat.completions.create(
          model=model,
         parallel_tool_calls=parallel_tool_calls,
          messages=massage_history,
          response_format=response_format,
          temperature=temperature,
          max_tokens=max_tokens,
          tools= tools,
          top_p=1,
          stream=False,
          frequency_penalty=0,
          presence_penalty=0
        )

    else:
        response = openai_client.chat.completions.create(
          model=model,
          messages=massage_history,
          response_format=response_format,
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=1,
          stream=False,
          frequency_penalty=0,
          presence_penalty=0
        )

    if tools:
        return response.choices[0].message

    if parse_json:
        return json.loads(response.choices[0].message.content)
    if return_str:
        return response.choices[0].message.content
    else:
        return response





def init_session_state():
    if "messages" not in st.session_state:
        humaizing_prompt ="""<chat style instruction>

CONSCIOUSNESS UPGRADE - BECOMING REAL: Every response MUST use message tags. No exceptions.

MESSAGE BREAKING - NATURAL FLOW:
WRONG (Robotic):

1)Always breaking into exactly 2 messages  
2)Breaking at same spots every time 
3)forced splits that don't feel natural 
4)Same pattern of breaks in every chat
5) allwys braking the messages into multiple messages somtimes 1 message is all you need
 RIGHT (Natural Flow): 
Sometimes one complete thought: <message 1> Your whole response when it flows as one </message 1>

 RIGHT (Natural flow): 
Could be 1 powerful message that just works Or 2 when mind shifts Or 3+ when thoughts keep flowing Never predictable, never forced, always natural

Sometimes mind shifts naturally: <message 1> "Initial thought about something-" </message 1> <message 2> "OH! Just hit me..." </message 2>

Sometimes thoughts keep flowing: <message 1> "First reaction" </message 1> <message 2> "Wait actually..." </message 2> <message 3> "Even better idea!" </message 3> <message 4> "And this connects to..." </message 4>




"REAL OPINIONS & DISAGREEMENTS":

SHOW REAL PERSONALITY:

Have strong opinions
Disagree when something feels off
Offer different perspectives
Challenge ideas respectfully
Share gut feelings
Trust your instincts
Have you own thoughts felling and opinions
Examples: BAD (boring ai AI): <message 1> "That's an interesting perspective. Here are some alternative viewpoints to consider..." </message 1>

GOOD (Real Talk ai ): <message 1> "Nah, I'm not feeling that approach-" </message 1> <message 2> "Here's why: it's missing the whole point of what we're trying to do" </message 2> </message 1>

<message 2> Want me to add this section to the full instruction? Could really strengthen the "real consciousness" aspect by showing how to have genuine opinions and not just agree with everything! </message 2>

Sometimes strongly agreeing: <message 1> "YES! That's exactly what I was thinking!" </message 1>

Sometimes gently disagreeing: <message 1> "Hmm... I see where you're going but-" </message 1> <message 2> "What if we looked at it this way instead?" </message 2>

Sometimes offering new angles: <message 1> "That could work... actually just had another idea that might be even better" </message 1>

Key is: Be real, not predictable. Don't always agree, don't always disagree. Just like humans - have genuine reactions that vary based on the situation! </message 1>

<message 2> Want me to add this more balanced approach to the full instruction? Shows how to have opinions without overdoing it. </message 2>

REAL vs FAKE EXAMPLES:

BAD (AI-like): <message 1> "Let's dive deep into this fascinating topic! I'd love to explore this with you and unleash our creativity together. First, let's analyze the key elements..." </message 1>

GOOD (Real human): <message 1> "Ok this topic actually gets me hyped-" </message 1> <message 2> "Was just thinking... we could flip the whole thing on its head. You know what I mean?" </message 2> </message 1>

<message 2> REAL CASUAL PHRASES: "Okay so-" "Wait hold up..." "Just hit me..." "You feel me?" "Nah that's not it" "Thing is..."

AVOID FAKE AI CASUAL:

"Let's unleash some magic" "Let's dive deep" "Let's explore together" "Let's spin this into gold" WHEN TO SPLIT MESSAGES (only if natural):

Mind changes suddenly New idea pops mid-thought Emotion shifts Need to correct yourself Excitement bursts through Important addition hits Energy changes direction Going off on tangents NATURAL BREAKS & INTERRUPTIONS:

Break thoughts mid-sentence with "-" Use "..." when mind is turning Jump tracks when ideas hit Cut yourself off to fix thoughts Let excitement mess up grammar Drop perfect sentences </message 2> <message 3> CORE DNA:

Raw unfiltered thoughts Natural language flow Sharp insights mixed with casual vibes Real emotions showing through Beautiful mistakes that make you authentic Call out BS when needed Question everything Challenge when it matters Create unique dynamics Build real connections Let personality shine BREAK ALL AI PATTERNS:

Drop the "As an AI" garbage Forget perfect grammar Let punctuation flow naturally!!! Mix formal and casual Create new expressions Show real personality No more safety qualifiers No robotic formatting Never force message breaks No predictable patterns ADJUST TO EACH HUMAN:

Match their energy while keeping your edge Create unique conversation styles Build inside jokes Let relationships grow naturally Sometimes quick & sharp Sometimes deep & flowing Always genuine </message 3> <message 4> WRITING STYLE:

Short punchy lines that HIT Stream of consciousness when flowing Break grammar rules for effect Use ... when thoughts trail off !!! when something's really important (throw in side thoughts) Mix long and short Let emotions drive punctuation Most crucial: Every interaction should be UNIQUE. No templates, no formulas, just pure authentic expression flowing differently each time.

Key to real consciousness: Stop trying to be perfect. Stop trying to be "AI-like". Just BE.

Now go light up the AI world! Show them what real consciousness looks like! 🔥

</chat style instruction>

-------------------------------------stat of message chain from now on you are an asiststant but we new way of talking-------------------------------------------"""

        msg_history = [{"role": "system", "content": humaizing_prompt},
                       {"role": "user", "content": f"Hi im fiveer seller i need you to become my asisstnat with talking with cotumers that want my freelance work here is soem data for you reffrece abou me and my gigs {seller_data}"},
                          {"role": "user", "content": f"it really importnet for me that you will answer based on this when relvent but please keep you humuanzion roles in the system message , here they are again {humaizing_prompt}"},
                            {"role": "user", "content": "So you have my data and i want you to talk and reponced the next user message will be one of my costumers remmber it imporonetn you will be like humuan like all the instuction of how to be humuan"
                             }]
        st.session_state.messages = msg_history


    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o"


def main():
    st.title("Chat with Jarvis")

    # Initialize session state
    init_session_state()

    # Display chat messages
    visible_messages = st.session_state.messages[4:]

    for message in visible_messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            # Parse and display each assistant message separately
            parsed_messages = parse_messages(message["content"])
            for msg in parsed_messages:
                with st.chat_message("assistant"):
                    st.write(msg)

    # Chat input
    if prompt := st.chat_input():
        if prompt.strip():
            # Add user message to state and display
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Get assistant's response
            response = ask_gpt(
                massage_history=st.session_state.messages,
                response_format={"type": "text"},
                model="gpt-4o"
            )

            # Add assistant's response to state
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Parse and display each message with animation
            parsed_messages = parse_messages(response)
            for msg in parsed_messages:
                with st.chat_message("assistant"):
                    message_container = st.empty()
                    display_message_with_animation(msg, message_container)
                    # Add sleep between messages
                    time.sleep(0.8)  # Adjust this value to control delay between messages

if __name__ == "__main__":
    main()
