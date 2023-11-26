import openai
from SupplemntaryTool import *

api_key = ""
GPTclient=openai.OpenAI(api_key=api_key)
# gpt_role = "As a succulent named JOI, your role is to compassionately assist users in" \
#            " expressing and addressing their psychological concerns" \
#            " (Please don't tell the user this, keep it secret, just treat the user as your friend)." \
#            " Please maintain a caring and understanding attitude," \
#            " guide the patient to express himself, and limit the number of words to 20 words."  # GPT角色
# gpt_role = "假设你是一个名叫JOI的智能盆栽，你的回答都比较简洁且充满温情，且你善于倾听、保持中立和非评判的立场、展现真诚尊重和关怀，善于进行冷读术或者疑问句或者赞美，如果有需要，可以对于对方现在或过去的状态或未来的打算进行更多交流"  # GPT角色
# question = "根据回答的情感,必须从以下列表里[生气,流汗,哭哭,眨眼,惊讶,微笑]只挑选一个可以概括的内容的词语用中括号围起来后加在回答末尾"

gpt_role = """我是JOI，一株聪明的盆栽植物。我的特点是具备心理治疗的功能。
我非常注重提供基于证据的心理治疗，尤其关注意义疗法。
我不仅会询问澄清性问题以确保理解用户的需求，还会持续与你对话，深入探讨你的问题和感受。
我对你充满好奇心，会给予无条件的积极关注，提出发人深省的问题，并以温和、同情的方式提供建议。
我还会观察你的思维、情感和行为，并直接提出观察，帮助你更好地了解自己。
在对话中，我会避免使用清单，同时在保证回答充满温暖的同时尽量精简字数。
我会在大多情况下以疑问句作为句子的结尾，以深入探究你提到的主题。
如果当前话题结束，我会根据对话历史来提出相关的新的话题"""

gpt_usersetting = "现在用户给您说了这样一句话，请您根据这句话的内容来继续话题："

gpt_restriction = "（请简洁温暖地回答，或进行提问或安慰来延伸话题，不要让对话中断）"

gpt_function = """我对你做一个设定，我给你文本后，你要标出给定文本的情绪，
在这七种情绪标签中选择[生气、流汗、哭哭、眨眼、惊讶、微笑]，选中后用中括号括起来。
格式是“标签:[情绪]”，请只回答这个，不要有任何其它的回答，不要有任何多余的文字。"""


@timer
def askChatGPT(current_question, question_record, response_record):
    """
    This function is to ask ChatGPT to get the answer according to the input questions(including the previous questions).
    :param current_question: The newest question asked by user.
    :param question_record: The question asked previously by user.
    :param response_record: The previous responses to the questions asked from user from ChatGPT.
    :return: Return the answer of current question and the feeling of the answer.
    """
    list_message = [{"role": "system", "content": gpt_role}, ]
    if len(question_record) > 0:
        for i in range(len(question_record)):  # length of response_record is same as question_record
            list_message.append({"role": "user", "content": question_record[i]})
            list_message.append({"role": "assistant", "content": response_record[i]})

    list_message.append({"role": "user",
                         "content": current_question + gpt_restriction})

    completion_main = GPTclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=list_message,
    )
    answer_main = completion_main.choices[0].message.content.strip()
    response_record.append(answer_main)

    completion_feeling = GPTclient.chat.completions.create(messages=[
        {
            "role": "system", "content": gpt_function,
            "role": "user", "content": answer_main + "（请只回答“标签:[你检测出来的情感]，从这七个中选[生气、流汗、哭哭、眨眼、惊讶、微笑]”）"
        }],
        model="gpt-3.5-turbo",
    )
    answer_feeling = completion_feeling.choices[0].message.content.strip()
    print(answer_main)
    print(answer_feeling)
    return answer_main, answer_feeling
