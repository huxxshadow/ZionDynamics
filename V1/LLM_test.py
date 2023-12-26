from LLM import *

def main():
    # 初始化问题和回答的记录
    question_record = []
    response_record = []

    while True:
        # 获取用户输入
        user_input = input("请输入您的问题（输入'exit'退出）: ")

        # 检查是否退出
        if user_input.lower() == 'exit':
            print("对话结束。")
            break

        # 调用 askChatGPT 函数获取回答
        answer, feeling = askChatGPT(user_input, question_record, response_record)

        # 更新记录
        question_record.append(user_input)
        response_record.append(answer)

if __name__ == "__main__":
    main()