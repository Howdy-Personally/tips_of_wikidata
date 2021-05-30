import json
import time
import argparse
import pymysql
import os
import sys


def create_tables():

    #link to db
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
    #curs obj
    cur = conn.cursor()

    # create entitles table;
    sql="create table if not exists entitles(type VARCHAR(10),entitles_id VARCHAR(10) Primary Key,\
        en_labels VARCHAR(255),zh_labels VARCHAR(255),en_descriptions VARCHAR(511),zh_descriptions VARCHAR(255));"
    cur.execute(sql)

    # create en_aliases table;
    sql="create table if not exists en_aliases(entitles_id VARCHAR(10),property_id VARCHAR(10),en_aliases VARCHAR(255));"
    cur.execute(sql)

    # create zh_aliases table;
    sql="create table if not exists zh_aliases(entitles_id VARCHAR(10),property_id VARCHAR(10),zh_aliases VARCHAR(255));"
    cur.execute(sql)

    # create property table;
    sql="create table if not exists property(type VARCHAR(10),property_id VARCHAR(10) Primary Key,\
        en_labels VARCHAR(255),zh_labels VARCHAR(255),en_descriptions VARCHAR(511),zh_descriptions VARCHAR(255));"
    cur.execute(sql)

    # create claims
    sql="create table if not exists claims(entitles_id VARCHAR(10),property_id VARCHAR(10) ,value VARCHAR(1023),claims_id VARCHAR(100) Primary Key);"
    cur.execute(sql)

    # create qualifiers
    sql="create table if not exists qualifiers(claims_id VARCHAR(100),property_id VARCHAR(10),quali_hash VARCHAR(100) primary key,value VARCHAR(1023));"
    cur.execute(sql)

    # create references
    sql="create table if not exists reference(claims_id VARCHAR(100),property_id VARCHAR(10),refer_hash VARCHAR(100),value VARCHAR(1023));"
    cur.execute(sql)


    #close curs obj
    cur.close()
    #close db
    conn.close

def store_to_db_aliases(db_entitles_id,db_property_id,line,opt):
    db_en_aliases='null'
    db_zh_aliases='null'

    for key in line:
        if key=='en':
            for iter in line[key]:
                if not '\\u' in json.dumps(iter):# delete error char
                    db_en_aliases=iter['value']
                    if "\\"in db_en_aliases:
                        db_en_aliases=db_en_aliases.replace('\\','/')
                    if "\'" in db_en_aliases:
                        db_en_aliases=db_en_aliases.replace('\'','\\\'')
                        # print(db_en_aliases)

                    sql = "INSERT INTO en_aliases(entitles_id, property_id, en_aliases)SELECT '"+\
                        db_entitles_id+"', '"+db_property_id+"', '"+db_en_aliases+\
                        "'FROM dual WHERE not exists (select * from en_aliases where en_aliases.en_aliases='"+db_en_aliases+"');"
                    opt.error_sql=sql
                    # INSERT INTO en_aliases(entitles_id, property_id, en_aliases)
                    # SELECT '1', '1', '1'FROM dual WHERE not exists 
                    # (select * from en_aliases where en_aliases.entitles_id='1');
                    
                    #link to db
                    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
                    #curs obj
                    cur = conn.cursor()
                    #execute sql
                    cur.execute(sql)
                    #close curs obj
                    cur.close()
                    #close db
                    conn.close

        if key=='zh-hans':
            for iter in line[key]:
                db_zh_aliases=iter['value']
                if "\'" in db_zh_aliases:
                        db_zh_aliases=db_zh_aliases.replace('\'','\\\'')

                sql = "INSERT INTO zh_aliases(entitles_id, property_id, zh_aliases)SELECT '"+\
                    db_entitles_id+"', '"+db_property_id+"', '"+db_zh_aliases+\
                    "'FROM dual WHERE not exists (select * from zh_aliases where zh_aliases.zh_aliases='"+db_zh_aliases+"');"
                opt.error_sql=sql
                #link to db
                conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
                #curs obj
                cur = conn.cursor()
                #execute sql
                cur.execute(sql)
                #close curs obj
                cur.close()
                #close db
                conn.close

def store_to_entitles_property(line,opt):

    for key in line:
        if key == 'type':
            db_type = line[key]

        if key =='id':
            db_entitles_property_id=line[key]

        if key =='labels':
            db_en_labels='null'
            db_zh_labels='null'
            for iter in line[key]:
                if iter=='en':
                    db_en_labels=line[key][iter]['value']
                    if "\'" in db_en_labels:
                        db_en_labels=db_en_labels.replace('\'','\\\'')
                if iter=='zh-hans':
                    db_zh_labels=line[key][iter]['value']
                    if "\'" in db_zh_labels:
                        db_zh_labels=db_zh_labels.replace('\'','\\\'')
            
        if key =='descriptions':
            db_en_descriptions='null'
            db_zh_descriptions='null'
            for iter in line[key]:
                if iter=='en':
                    db_en_descriptions=line[key][iter]['value']
                    if "\'" in db_en_descriptions:
                        db_en_descriptions=db_en_descriptions.replace('\'','\\\'')
                if iter=='zh-hans':
                    db_zh_descriptions=line[key][iter]['value']
                    if "\'" in db_zh_descriptions:
                        db_zh_descriptions=db_zh_descriptions.replace('\'','\\\'')
                    

        if key =='aliases':
            store_to_db_aliases(db_entitles_property_id,'null',line[key],opt)

        if key =='claims':
            store_to_claims(line,opt)

    # store to entitles && properties
    if opt.table=='entitles':
        sql = "INSERT INTO entitles(type, entitles_id, en_labels, zh_labels, en_descriptions, zh_descriptions)SELECT '"+\
            db_type+"', '"+db_entitles_property_id+"', '"+db_en_labels+"', '"+db_zh_labels+"', '"+db_en_descriptions+"', '"+db_zh_descriptions+\
            "'FROM dual WHERE not exists (select * from entitles where entitles.entitles_id='"+db_entitles_property_id+"');"
    
    else:# table = property
        sql = "INSERT INTO property(type, property_id, en_labels, zh_labels, en_descriptions, zh_descriptions)SELECT '"+\
            db_type+"', '"+db_entitles_property_id+"', '"+db_en_labels+"', '"+db_zh_labels+"', '"+db_en_descriptions+"', '"+db_zh_descriptions+\
            "'FROM dual WHERE not exists (select * from property where property.property_id='"+db_entitles_property_id+"');"
    

    opt.error_sql=sql
    #link to db
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
    #curs obj
    cur = conn.cursor()
    #execute sql
    cur.execute(sql)
    #close curs obj
    cur.close()
    #close db
    conn.close
    # store to entitles && properties


def store_to_claims_mainsnak(entitles_id,line,claims_id,opt):
    claims_mainsnak_value='null'
    for key in line:
        if key=='property':
            property_id=line[key]
        if key=='datavalue':
            for iter in line[key]:
                if iter=='value':
                    if(type(line[key][iter]))==str:
                        claims_mainsnak_value=line[key][iter]
                    if(type(line[key][iter]))==dict:
                        for alter in line[key][iter]:
                            if alter=='id'or alter=='time'or alter=='amount':
                                claims_mainsnak_value=line[key][iter][alter]

    if '\\u' in json.dumps(claims_mainsnak_value):
        claims_mainsnak_value='null'
    if '\'' in claims_mainsnak_value:
        claims_mainsnak_value=claims_mainsnak_value.replace('\'','\\\'')
        # if line[key] =='P898':
        #     sys.exit()

    # print(entitles_id,property_id,claims_mainsnak_value,claims_id)

    
    # store to claims mainsnak
    sql = "INSERT INTO claims(entitles_id, property_id, value, claims_id)SELECT '"+\
        entitles_id+"', '"+property_id+"', '"+claims_mainsnak_value+"', '"+claims_id+\
        "'FROM dual WHERE not exists (select * from claims where claims.claims_id='"+claims_id+"');"
    # print(sql)
    opt.error_sql=sql
    #link to db
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
    #curs obj
    cur = conn.cursor()
    #execute sql
    cur.execute(sql)
    #close curs obj
    cur.close()
    #close db
    conn.close

def store_to_claims_qualifiers(claims_id,line,opt):
    claims_qualifiers_value='null'
    property_id=''
    quali_hash=''
    for key in line:
        for iter in line[key]:
            for alter in iter:
                property_id=iter['property']
                quali_hash=iter['hash']
                if alter=='datavalue':
                    for monitor in iter[alter]:
                        if monitor =='value':
                            if type(iter[alter][monitor])==str:
                                claims_qualifiers_value=iter[alter][monitor]
                            if type(iter[alter][monitor])==dict:
                                for camera in iter[alter][monitor]:
                                    if camera =='id'or camera=='time'or camera=='amount':
                                        claims_qualifiers_value=iter[alter][monitor][camera]
                                        
    if '\'' in claims_qualifiers_value:                                  
        claims_qualifiers_value=claims_qualifiers_value.replace('\'','\\\'')
    # print(claims_id,property_id,quali_hash,claims_qualifiers_value)

    # store to claims qualifiers
    sql = "INSERT INTO qualifiers(claims_id, property_id, quali_hash, value)SELECT '"+\
        claims_id+"', '"+property_id+"', '"+quali_hash+"', '"+claims_qualifiers_value+\
        "'FROM dual WHERE not exists (select * from qualifiers where qualifiers.quali_hash='"+quali_hash+\
            "');"
    # print(sql)
    opt.error_sql=sql
    #link to db
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
    #curs obj
    cur = conn.cursor()
    #execute sql
    cur.execute(sql)
    #close curs obj
    cur.close()
    #close db
    conn.close
    # store to claims qualifiers

                # sys.exit()


def store_to_claims_references(claims_id,line,opt):
    claims_references_value='null'
    property_id=''
    refer_hash=''
    for key in line:
        refer_hash=key['hash']
        for iter in key['snaks']:
            for alter in key['snaks'][iter]:
                property_id=alter['property']
                for monitor in alter:
                    if monitor =='datavalue':
                        if(type(alter[monitor]))==str:
                            claims_references_value=alter[monitor]
                        if(type(alter[monitor]))==dict:
                            for camera in alter[monitor]['value']:
                                if camera =='id'or camera=='time'or camera=='amount':
                                    claims_references_value=alter[monitor]['value'][camera]
            
            #print(claims_id,property_id,refer_hash,claims_references_value)
            
            sql = "INSERT INTO reference(claims_id, property_id, refer_hash, value)SELECT '"+\
            claims_id+"', '"+property_id+"', '"+refer_hash+"', '"+claims_references_value+\
            "'FROM dual WHERE not exists (select * from reference where reference.property_id='"+property_id+"'"+\
                "and reference.refer_hash='"+refer_hash+"'"+"and reference.value='"+claims_references_value+"');"
    
            opt.error_sql=sql
            #link to db
            conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
            #curs obj
            cur = conn.cursor()
            #execute sql
            cur.execute(sql)
            #close curs obj
            cur.close()
            #close db
            conn.close
            # store to entitles



def store_to_claims(line,opt):
    quali=0
    refer=0
    for key in line:
        if key =='id':
            db_entitles_id=line[key]

        if key == 'claims':
            for iter in line[key]:
                for alter in line[key][iter]:
                    for monitor in alter:
                        if monitor =='id':
                            claims_id=alter[monitor]
                            store_to_claims_mainsnak(db_entitles_id,alter['mainsnak'],claims_id,opt)
                            
                        if monitor =='qualifiers':
                            quali=1
                        if monitor =='references':
                            refer=1

                    if quali==1:
                        quali=0
                        store_to_claims_qualifiers(claims_id,alter['qualifiers'],opt)
                    if refer==1:
                        refer=0
                        store_to_claims_references(claims_id,alter['references'],opt)

                

def store_to_db_entitles(opt):
 #load
    with open(opt.qitem_path, 'r',encoding='utf-8') as pf:
        j = 0
        for line in pf:
            j+=1
            try:
                # time.sleep(.5)
                line = line.replace('\\\\','\\').replace('\\\'','\'')
                line = json.loads(line)
                opt.table='entitles'
                store_to_entitles_property(line,opt)
                # store_to_claims(line,opt)
                if j%1000==0:
                    print(time.asctime(),'line',j,'stored')

            #load
            except Exception :
                print(j,'error')
                print(opt.error_sql)
                pass
        print(time.asctime(),'and line %s entitles all stored'%j)


def store_to_db_property(opt):
 #load
    with open(opt.pid_path, 'r',encoding='utf-8') as pf:
        j = 0
        for line in pf:
            j+=1
            try:
                # time.sleep(.5)
                line = line.replace('\\\\','\\').replace('\\\'','\'')
                line = json.loads(line)
                opt.table='property'
                store_to_entitles_property(line,opt)
                if j%1000==0:
                    print(time.asctime(),'and line',j,'stored')

                
            #load
            except Exception :
                print(j,'error')
                print(opt.error_sql)
                pass
        print(time.asctime(),'and line %s properties all stored'%j)

def test(opt):# 特殊中文不能存
    # store to entitles
    opt.table='entitles'
    sql = "INSERT INTO property(type,property_id, en_labels, zh_labels,en_descriptions,zh_descriptions)SELECT 'property', \
    'P2717', 'no-observed-adverse-effect level', 'null', 'greatest concentration or amount of a substance, found by experiment or observation,\
         which causes no detectable adverse alteration of morphology, functional capacity, growth, development,\
              or life span of the target organism under defined conditions of exposure', \
    'null'FROM dual WHERE not exists (select * from property where property.property_id='P2717');"
    opt.error_sql=sql
    #link to db
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',charset="utf8",db='wikidata',autocommit=True)
    #curs obj
    cur = conn.cursor()
    #execute sql
    cur.execute(sql)
    #close curs obj
    cur.close()
    #close db
    conn.close
    # store to entitles

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--qitem_path', type=str, default='./line_10000_file.json', help='qitem data path')
    parser.add_argument('--pid_path', type=str, default='./pid_file.json', help='pid data path')
    parser.add_argument('--table', type=str, default='', help='table')
    parser.add_argument('--error_sql', type=str, default='', help='error sql')

    opt=parser.parse_args()
    os.chdir("C:/Users/123/Desktop/wikidata")
    print(time.asctime(),'store start')
    create_tables()
    # # test(opt)
    store_to_db_entitles(opt)
    store_to_db_property(opt)
    print(time.asctime(),'store end')