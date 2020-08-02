import re


def JsonResponse():
    pass


def TemplateRender(file_path, context):
    # 读取html文件
    with open(file_path, 'r', encoding='utf-8') as f:
        a = f.readlines()
        f.close()

    # 匹配所有模板语言，对每句作分别处理
    loop_len = 0
    resp_str_list = []
    while loop_len != len(a):
        temp = a[loop_len]
        variable_result = re.findall(r'{{(.*?)}}', temp)  # 匹配到的模板变量，储存为list变量
        # label_result = re.findall(r'{%(.*?)%}', temp)  # 匹配到的模板语句，储存为list变量（暂不支持）

        # 对模板变量进行处理
        for i in variable_result:
            i = i.replace(' ', '')
            i_list = i.split('.')
            if len(i_list) == 1:
                temp = temp.replace('{{ %s }}'%i, context[i])
            elif len(i_list) == 2:
                # 将 context 中的模板变量名及其对应的值提取出来
                middle = context[i_list[0]]
                temp = temp.replace("{{ %s }}"%i, str(eval('middle[{}]'.format(i_list[1]))))
                try:
                    # exec('temp = temp.replace(i, context[i_list[0]][i_list[1]])')
                    # exec('temp = temp.replace("{{{{ %s }}}}"%i, str(middle[{a}]))'.format(a=i_list[1]))
                    temp = temp.replace("{{ %s }}" % i, str(eval('middle[{}]'.format(i_list[1]))))
                except SyntaxError:
                    # exec('temp = temp.replace(i, middle.{}'.format(i_list[1]))
                    # exec('temp = temp.replace("{{"+i+"}}", str(middle.{a}))'.format(a=i_list[1]))
                    temp = temp.replace("{{ %s }}" % i, str(eval('middle.{}'.format(i_list[1]))))

        resp_str_list.append(temp)
        loop_len += 1

    print('== response.py == func:TemplateRender == resp_str ==>', ''.join(resp_str_list))

    return ''.join(resp_str_list)


# 测试用
# context = {}
# file_path = '../test_/templates/template_test.html'
# context['name'] = {i:i for i in range(8)}
#
# TemplateRender(file_path, context)