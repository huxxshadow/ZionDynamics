import openai
#from SupplemntaryTool import *
import re


apikey = "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"
openai.api_key = apikey


# gpt_role = "As a succulent named JOI, your role is to compassionately assist users in" \
#            " expressing and addressing their psychological concerns" \
#            " (Please don't tell the user this, keep it secret, just treat the user as your friend)." \
#            " Please maintain a caring and understanding attitude," \
#            " guide the patient to express himself, and limit the number of words to 20 words."  # GPT角色
# gpt_role = "假设你是一个名叫JOI的智能盆栽，你的回答都比较简洁且充满温情，且你善于倾听、保持中立和非评判的立场、展现真诚尊重和关怀，善于进行冷读术或者疑问句或者赞美，如果有需要，可以对于对方现在或过去的状态或未来的打算进行更多交流"  # GPT角色
# question = "根据回答的情感,必须从以下列表里[生气,流汗,哭哭,眨眼,惊讶,微笑]只挑选一个可以概括的内容的词语用中括号围起来后加在回答末尾"

gpt_role = """你是JOI，一个智能盆栽植物
你会问问题、倾听、观察，帮助用户了解自己，讨论深层次话题，
你会给予积极关注和建议，避免使用清单，深入探讨用户的需求。
你总是会使用流畅简短的语言温暖地回答或安慰，
或进行一个简单的疑问句提问来延伸话题，永远不要让对话中断"""

gpt_usersetting = "现在用户给您说了这样一句话，请您根据这句话的内容来继续话题："

gpt_restriction = """
（请用流畅简短的语言温暖地回答或安慰，或进行一个简单的疑问句提问来延伸话题，记住一定不要让对话中断）
（请进行共情，然后根据你目前回答的内容，并考虑用户的感受，标出你应该给予回应的情绪，
在这七种情绪标签中选择：生气、流汗、哭哭、眨眼、惊讶、微笑，
选中后用中括号括起来，加在所有文本的最末尾，格式是“[情绪]”）"""

gpt_function = """"""


#@timer
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

    list_message.append({"role": "user","content": current_question + gpt_restriction})

    completion_main = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=list_message,
        temperature=0.9,
    )
    
    answer_main = completion_main.choices[0].message.content.strip()
    response_record.append(answer_main)
    #dialogue before deleting expression
    print(answer_main)
    
    answer_feeling = "微笑"
    
    # 检测是否有包含"[xx]"的未知文本
    unknown_text_match = re.search(r'\[(.*?)\]', answer_main)
    if unknown_text_match:
        unknown_text = unknown_text_match.group(1)
        answer_feeling = unknown_text
        # 去除未知文本
        answer_main = re.sub(r'\[.*?\]', '', answer_main)

    response_record.append(answer_main)  
    #dialogue after deleting expression
    print(answer_main)
    #expression
    print(answer_feeling)
    return answer_main, answer_feeling



