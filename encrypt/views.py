from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.db import connections
import subprocess
from threading import Thread
import Queue
import pandas as pd
from django.core.files.storage import FileSystemStorage
import namegenerator
import os
import numpy
# from django.forms import UploadFileForm
# Create your views here.


@csrf_exempt
def encrypt(request):
    if request.method == 'POST':
        file = request.FILES['file']
        print(file)
        fs = FileSystemStorage()
        generated_name = namegenerator.gen()
        gen_name = str(generated_name) + '.txt'
        filename = fs.save(gen_name, file)
        uploaded_file_url = fs.url(filename)
        type = check_file_type(uploaded_file_url)
        #os.remove("." + str(uploaded_file_url))
        if type == 'none':
            # os.remove(uploaded_file_url)
            return render(request, "encrypt.html", {'message': "Invalid file type"})
        uploaded_file_url = '.' + uploaded_file_url
        f = open(uploaded_file_url, 'r')
        a = f.read()
        list = a.split()
        plaintext_list = []
        for i in list:
            #j = str(i, 'utf-8')
            plaintext_list.append(i)
        print(plaintext_list)
        del list

        md5_queue = Queue.Queue(maxsize=0)
        sha1_queue = Queue.Queue(maxsize=0)
        sha224_queue = Queue.Queue(maxsize=0)
        sha256_queue = Queue.Queue(maxsize=0)
        sha384_queue = Queue.Queue(maxsize=0)

        md5_list = Thread(target=viewsMd5, args=(plaintext_list, md5_queue,))
        sha1_list = Thread(viewsSha1(plaintext_list, sha1_queue))
        sha224_list = Thread(viewsSha224(plaintext_list, sha224_queue))
        sha256_list = Thread(viewsSha256(plaintext_list, sha256_queue))
        sha384_list = Thread(viewsSha384(plaintext_list, sha384_queue))

        md5_list.start()
        sha1_list.start()
        sha224_list.start()
        sha256_list.start()
        sha384_list.start()

        md5_list.join()
        sha1_list.join()
        sha224_list.join()
        sha256_list.join()
        sha384_list.join()

        md5_lst = []
        sha1_lst = []
        sha224_lst = []
        sha256_lst = []
        sha384_lst = []

        while sha384_queue.empty() != True:
            md5_lst.append(md5_queue.get())
            sha1_lst.append(sha1_queue.get())
            sha224_lst.append(sha224_queue.get())
            sha256_lst.append(sha256_queue.get())
            sha384_lst.append(sha384_queue.get())

            md5_queue.task_done()
            sha1_queue.task_done()
            sha224_queue.task_done()
            sha256_queue.task_done()
            sha384_queue.task_done()

        id = pushData(plaintext_list, md5_lst, sha1_lst,
                      sha224_lst, sha256_lst, sha384_lst)
        updated_list = '[+] Updated hash size : ' + str(id)
        return render(request, "encrypt.html", {'message': "success", 'id': updated_list})
    else:
        return render(request, 'encrypt.html')


def check_file_type(uploaded_file_url):
    command = 'file .' + str(uploaded_file_url)
    output = subprocess.getoutput(command)
    print(output)

    if 'ASCII text' in output:
        return 'text'
    else:
        return 'none'


def viewsMd5(lst, md5):
   # md5_list = []
    for i in lst:
        md5_hash = hashlib.md5(i.encode()).hexdigest()
        print(md5_hash)
        print('hello')
        md5.put(md5_hash)


def viewsSha1(lst, sha1_list):
   # sha1_list = []
    for i in lst:
        sha1_hash = hashlib.sha1(i.encode()).hexdigest()
        sha1_list.put(sha1_hash)
   # return sha1_list


def viewsSha224(lst, sha224_list):
   # sha224_list = []
    for i in lst:
        sha224_hash = hashlib.sha224(i.encode()).hexdigest()
        sha224_list.put(sha224_hash)
    # return sha224_list


def viewsSha256(lst, sha256_list):
   # sha256_list = []
    for i in lst:
        sha256_hash = hashlib.sha256(i.encode()).hexdigest()
        sha256_list.put(sha256_hash)
   # return sha256_list


def viewsSha384(lst, sha384_list):
    # sha384_list = []
    for i in lst:
        sha384_hash = hashlib.sha384(i.encode()).hexdigest()
        sha384_list.put(sha384_hash)
   # return sha384_list


def pushData(plaintext_list, md5_list, sha1_list, sha224_list, sha256_list, sha384_list):
    cursor = connections['default'].cursor()
    cursor.fast_executemany = True

    if len(plaintext_list) > 100000:
        data_size = len(plaintext_list)
        plaintext_data = numpy.array(plaintext_list)
        md5_data = numpy.array(md5_list)
        sha1_data = numpy.array(sha1_list)
        sha224_data = numpy.array(sha224_list)
        sha256_data = numpy.array(sha256_list)
        sha384_data = numpy.array(sha384_list)

        no_of_sets = int(len(plaintext_data)/100000)

        if len(plaintext_list) % 100000 != 0:
            no_of_sets = no_of_sets + 1

        plaintext_lst = numpy.array_split(plaintext_list, no_of_sets)
        md5_lst = numpy.array_split(md5_list, no_of_sets)
        sha1_lst = numpy.array_split(sha1_list, no_of_sets)
        sha224_lst = numpy.array_split(sha224_list, no_of_sets)
        sha256_lst = numpy.array_split(sha256_list, no_of_sets)
        sha384_lst = numpy.array_split(sha384_list, no_of_sets)

        for i in range(no_of_sets):
            last_id_query = "SELECT id FROM encrypt_hashes ORDER BY id DESC LIMIT 1;"
            cursor.execute(last_id_query)
            try:
                last_id = int(cursor.fetchall()[0][0])
            except:
                last_id = 0
            id = []
            for j in range(last_id+1, len(plaintext_lst[i])+last_id+1):
                id.append(j)
            df = pd.DataFrame(list(zip(id, md5_lst[i], plaintext_lst[i], sha1_lst[i], sha224_lst[i], sha256_lst[i], sha384_lst[i])), columns=[
                'id', 'md5', 'plain_text', 'sha1', 'sha224', 'sha256', 'sha384'])
            print(df)
            df.to_csv('./uploads/file.csv', index=False)

            insert_query = "LOAD DATA LOCAL INFILE '/home/srihari/Documents/bca_project/HashEngine/uploads/file.csv' INTO TABLE encrypt_hashes fields terminated by ',' lines terminated by '\n' ignore 1 rows;"

            cursor.execute(insert_query)

    else:
        last_id_query = "SELECT id FROM encrypt_hashes ORDER BY id DESC LIMIT 1;"
        cursor.execute(last_id_query)
        try:
            last_id = int(cursor.fetchall()[0][0])
        except:
            last_id = 0
        id = []
        for i in range(last_id+1, len(plaintext_list)+last_id+1):
            id.append(i)
        df = pd.DataFrame(list(zip(id, md5_list, plaintext_list, sha1_list, sha224_list, sha256_list, sha384_list)), columns=[
            'id', 'md5', 'plain_text', 'sha1', 'sha224', 'sha256', 'sha384'])
        print(df)
        df.to_csv('./uploads/file.csv', index=False)

        insert_query = "LOAD DATA LOCAL INFILE '/home/srihari/Documents/bca_project/HashEngine/uploads/file.csv' INTO TABLE encrypt_hashes fields terminated by ',' lines terminated by '\n' ignore 1 rows;"

        cursor.execute(insert_query)

        cursor.execute(last_id_query)
        try:
            last_id = int(cursor.fetchall()[0][0])
        except:
            last_id = 0

        return last_id

    # os.remove('./uploads/file.csv')
    # for i in range(len(md5_list)):
    #     plain = plaintext_list[i]
    #     md5 = md5_list[i]
    #     sha1 = sha1_list[i]
    #     sha224 = sha224_list[i]
    #     sha256 = sha256_list[i]
    #     sha384 = sha384_list[i]
    # chunk = df.iloc[i:i + 1, :].values.tolist()
    # values = tuple(tuple(x) for x in chunk)
    # sql = "insert into encrypt_hashes(md5,plain_text,sha1,sha224,sha256,sha384) values(%s,%s,%s,%s,%s,%s)"
    # values = (md5, plain, sha1, sha224, sha256, sha384)
    # cursor.execute(sql, values)
    # print(cursor.rowcount, "record inserted.")


def home(request):
    return render(request, "home.html")


def decrypt(request):
    if request.method == 'POST':
        hash = request.POST.get('hash')
        hash_type = get_hash_type(hash)
        if hash_type == "None":
            return render(request, "decrypt.html", {'message': "[+] Unable to recognise hash type"})
        else:
            plain_text = get_plain_text(hash, hash_type)
            if len(plain_text) == 0:
                return render(request, "decrypt.html", {'message': "[+] Hash not found", 'hash_type': "Hash type : " + str(hash_type)})
            else:
                text = plain_text[0]
                return render(request, "decrypt.html", {'hash_message': '[+] Hash Found', 'hash_type': "Hash type : " + str(hash_type), 'message': str(text[0])})

    else:
        return render(request, "decrypt.html")


def get_hash_type(hash):
    command = "hashid -j " + str(hash)
    hashid_output = subprocess.getoutput(command)
    if "raw-sha1" in hashid_output:
        return "sha1"
    elif "raw-md5" in hashid_output:
        return "md5"
    elif "raw-sha224" in hashid_output:
        return "sha224"
    elif "raw-sha256" in hashid_output:
        return "sha256"
    elif "raw-sha384" in hashid_output:
        return "sha384"
    else:
        return "None"


def get_plain_text(hash, hash_type):
    cursor = connections['default'].cursor()
    sql = "select plain_text from encrypt_hashes where " + \
        str(hash_type) + "=\"" + str(hash) + "\""
    cursor.execute(sql)
    output = cursor.fetchall()
    return output
