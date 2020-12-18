
import json
from collections import OrderedDict


def check_name(name):
    
    check_name_dict = {'to': 'tohex'}
    if name in check_name_dict:
        return check_name_dict[name]
    else:
        return name


def make_php(method, params):
    result = '\t//====================  \n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '$' + check_name(key) + ', '
    result = result + '\tfunction ' + method + '(' + tmp + ' &$data){ \n'
    result = result + '\t\t$js = $this->make_json (\'' + method + '\', array( '
    tmp = '\n'
    for key, value in params.items():
        tmp = tmp + '\t\t\t"' + key + '" => $' + check_name(key) + ',\n'

    result = result + tmp[:-2]
    result = result + '));\n'
    result = result + '\t\t return $this->request($js, $data); \n'
    result = result + '\t} \n'
    
    return result


def make_ruby(method, params):
    result = '\t#====================  \n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '' + check_name(key) + ', '
    tmp = tmp[:-2]
    result = result + '\tdef ' + method + '(' + tmp + ' ) \n'
    result = result + '\t\tjson=make_json(\'' + method + '\',{\n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '\t\t\t\'' + key + '\' : ' + check_name(key) + ',\n'

    result = result + tmp[:-2] + '\n'
    result = result + '\t\t})\n'
    result = result + '\t\tputs (\'' + method + '  method call\' )\n'
    result = result + '\t\tresult = make_request(json)    \n'
    result = result + '\t\treturn result\n'
    result = result + '\tend\n'
    return result


def make_python(method, params):
    result = ' \n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + ', ' + check_name(key) + ''

    result = result + '    def ' + method + '(self' + tmp + '): \n'
    result = result + '        data = {"jsonrpc": "2.0", "method": "' + method + '",\n'
    result = result + '                "params": {\n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '                     \'' + key + '\': '+check_name(key) + ',\n'

    result = result + tmp[:-2] + '\n'
    result = result + '                          },\n'
    result = result + '                "filter": self.genericfilter\n'
    result = result + '                }\n'
    result = result + '        logging.info(u\'' + method + ' method call\')\n'
    result = result + '        return self.send_request(data)\n'
    return result


def make_perl(method, params):
    result = 'sub '+method+' {  \n'
    result = result + '\tmy $self      = shift;\n'
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '\tmy $' + check_name(key) + '=shift;\n'
    result = result+tmp
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '\'' + key + '\' => $' + check_name(key) + ','

    result = result + '\tmy %params = (' + tmp[:-1] + ');\n'
    result = result + '\tmy $result = $self->postApi(\'' + method + "\', \%params);\n"
    result = result + '\treturn $result;\n'
    result = result + '}\n'
    return result


def make_bash(method, params):
    result = '\n'
    result = result + '' + method + '() {\n'
    result = result + 'param=$(./jq -n "{'
    tmp = ''
    argument_id = 1
    for key, value in params.items():
        tmp = tmp + '' + key + ': \\"$' + str(id) + '\\",'
        argument_id = argument_id + 1

    result = result + tmp[:-1]
    result = result + '}")\n'
    result = result + 'jsondata=$(makejson "' + method + '" "$param")\n'
    result = result + 'makerequest "$jsondata"\n'
    result = result + '}\n'
    return result


def make_asp(method, params):
    result = '\'-----------'+method+' -------------\n'

    tmp = ''
    for key, value in params.items():
        tmp = tmp + ' ' + check_name(key) + ','
    tmp = tmp[:-2]
    result = result + 'public Function api' + method + '(' + tmp + ' )\n'
    
    tmp = ''
    for key, value in params.items():
        tmp = tmp + '""' + key + '"":"""+' + check_name(key) + '""",'

    result = result + '\tapi' + method + ' = apiRequest(Session("mySessionId"), "'\
                    + method + '", "{ ' + tmp[:-1] + '}")\n'
    result = result + 'end function\n'
    return result


def generate_files(data, name, ext, filename):
    pre = open(name + '/pre.' + ext, 'r')
    post = open(name + '/post.' + ext, 'r')
    file = open(name + '/' + filename + '.' + ext, 'w')

    file.write(pre.read())
    for method in data:
        file.write(globals()["make_"+lang](method['method'], method['params'] if 'params' in method else {}))
        
    file.write(post.read())
    file.close()
    pre.close()
    post.close()


if __name__ == '__main__':
 
    with open('methods.json') as json_file:  
        methods = json.load(json_file, object_pairs_hook=OrderedDict)

    api_name = "sample"

    languages = {'asp': 'inc', 'bash': 'sh', "perl": "pm",
                 "python": "py", "ruby": "rb", "php": "php"}

    for lang in languages:
        generate_files(methods, lang, languages[lang], api_name)
