# 我需要当config.method = "get"时，按照AddSignToHeaders函数方式生成的nonce, timestamp和
# 一个键值对的形式，其中键为md5(nonce + timestamp)，值为encodeURIComponent(signature)
# 尽量简化，不需要传入config
# 我需要python，这些参数将作为我的request的请求参数
import hashlib
import time
import urllib.parse
import random
""" 
 generateNonce: function(n=16) {
        const t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let i = "";
        for (let r = 0; r < n; r++)
            i += t.charAt(Math.floor(Math.random() * t.length));
        return i
    },
"""

""" 
//按照key排序，并将键值对拼在一起变成字符串返回
    keyOrderWithData: function (dic) {
        //eg {x:2，y:3，z:1}
        var result = "sign_";
        if (!dic) {
            return result;
        }
        var sdic = Object.keys(dic).sort(function (a, b) { return a.localeCompare(b) });
        var value = "";

        if (!sdic) {
            return result;
        }


        for (var ki in sdic) {
            if (!sdic[ki] || typeof sdic[ki] === "function" || sdic[ki].indexOf("jQuery") === 0 || dic[sdic[ki]] === null || dic[sdic[ki]] === "" || dic[sdic[ki]] === undefined || dic[sdic[ki]] === "undefined" || typeof dic[sdic[ki]] === "function" || typeof dic[sdic[ki]] === "object") {
                continue;
            }
            else {
                value = dic[sdic[ki]];
            }

            result += sdic[ki] + value;
        }

        return result.replace(/\s/g, "").replace(/</g, "").replace(/>/g, "").replace(/\/>/g, "").replace(/\//g, "").replace(/[\n\r\u2028\u2029]+/g, '');;
    },
"""



""" 
/**
     * 添加签名到请求头
     * @param {Object} config 配置
     */
    function AddSignToHeaders(config) {
        var headers = config.headers;
        var nonce = Common.generateNonce();
        var timestamp = Common.generateTimestamp(); //时间戳精确到毫秒
        headers.common["nonce"] = nonce;
        headers.common["timestamp"] = timestamp;
        var dealedStrData = "";
        if (config.method === "get") {
            dealedStrData = Common.keyOrderWithData(config.params);
        } else {
            if (getDataType(config.data) === "object") {
                dealedStrData = Common.keyOrderWithData(config.data);
            } else {
                var newData = {};
                config.data.forEach((value, key) => {
                    newData[key] = value;
                })
                dealedStrData = Common.keyOrderWithData(newData);
            }
        }
        if (dealedStrData && dealedStrData != "") {
            var signature = md5(timestamp + nonce + dealedStrData);
            headers.common[md5(nonce + timestamp)] = encodeURIComponent(signature);
        }
    }
"""
def generate_nonce(n=16):
    """生成随机的nonce"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    nonce = ""
    for _ in range(n):
        nonce += random.choice(chars)
    return nonce

def generate_timestamp():
    """生成当前时间戳（毫秒）"""
    return int(time.time() * 1000)

def calculate_signature(timestamp, nonce, params):
    """计算签名"""
    # 按照key排序，并将键值对拼接成字符串
    ordered_params = sorted(params.items())
    ordered_str = ''.join(f'{k}{v}' for k, v in ordered_params)
    data_to_sign = f"{timestamp}{nonce}{ordered_str}"
    signature = hashlib.md5(data_to_sign.encode()).hexdigest()
    return urllib.parse.quote(signature)

def add_sign_to_headers(params):
    """根据给定的参数生成最终的键值对对象"""
    nonce = generate_nonce()
    timestamp = generate_timestamp()
    signature = calculate_signature(timestamp, nonce, params)

    key = hashlib.md5(f"{nonce}{timestamp}".encode()).hexdigest()
    return {
        key: signature, #签名
        "menucode": "08482E0F90AFB6F8",
        "nonce":nonce,  
        "timestamp":str(timestamp), # 时间戳精确到毫秒
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://eqstu.tfswufe.edu.cn/web/index.html"
    }

params = {
        "studentID": "122054",
        "semesterID": "2023-2024-2",
        "courseID": "846",
        "answerType": "308",
        "teachUnitID": "106634"
}


headers = add_sign_to_headers(params)
cookies = {
    "HomePageStyle": "default",
    "ASP.NET_SessionId": "wscl1knt55bzjwfccpuqizhy"
}
print(headers)



import requests
GetModuleUnitList = "https://eqstu.tfswufe.edu.cn/webapi/onlineTeaching/practice/GetModuleUnitList?semesterID=2023-2024-2&courseID=1283"


# 发送请求
re = requests.get(GetModuleUnitList, cookies=cookies)
print("状态码 :", re.status_code)
if re.status_code == 403:
    print("禁止访问: 访问被拒绝。没有足够的权限访问")
elif re.status_code == 401:
    print("未授权身份验证信息, cookies无效")

print("Response Headers :", re.headers)
print(re.text)

