import sys
import httplib2
import json
from tabulate import tabulate
from sets import Set
import os

class OpenDataFetcher:
    def __init__(self):
        self.root_url = "http://api.us.socrata.com/"
        self.domain_root = "api/catalog/v1/domains"
        self.query_root = "api/catalog/v1?domains="

        self.h = httplib2.Http(".cache")
        resp,content = self.h.request(self.root_url + self.domain_root)
        if not content:
          return None
        else:
          self.domains = json.loads(content)
          self.domains = self.domains['results'] #array of resource objects
        return

    def printDomainInfo(self):
        table_header = ["domain", "count"]
        table_data =[]
        for d in self.domains:
            row = []
            row.append(d['domain'])
            row.append(d['count'])
            table_data.append(row)
        print tabulate(table_data, table_header)

    def getInfo(self, domain=None, dataset_id=None, data_desc=False, get_data=False, _file=None):
        table_header = []
        table_data = []
        resources = None

        print "parameters [domain=" + domain + ", id=" + str(dataset_id)+ ", desc=" + str(data_desc) + \
                ", get_data=" + str(get_data) +"]"

        if domain is not None:
            if dataset_id is not None and get_data is False:
                resp,content=self.h.request(self.root_url+self.query_root+domain)
                if not content:
                    return None
                else:
                    resources = json.loads(content)
                    resources = resources["results"]
                    table_header = ["no. columns", "column names"]
                    for resObj in resources:
                        r = resObj['resource']
                        if r.has_key('id') and r['id']==dataset_id:
                            columnsObj = r['columns']
                            row = []
                            row.append(len(columnsObj.keys()))
                            row.append(columnsObj.keys())
                            table_data.append(row)
                            return tabulate(table_data,table_header)
            elif dataset_id is None and get_data is False:
                resp,content=self.h.request(self.root_url+self.query_root+domain)
                if not content:
                    return None
                else:
                    resources = json.loads(content)
                    resources = resources["results"]
                    table_header = ['id','description']
                    for resObj in resources:
                        r = resObj['resource']
                        row = []
                        if r.has_key('id') and r.has_key('description') and \
                           len(r['description'])>0:
                            row.append(r['id'])
                            row.append(r['description'])
                            table_data.append(row)
                    return tabulate(table_data, table_header)
            elif dataset_id is not None and get_data is True and dataset_id is not None:
                if dataset_id == '*':
                    resp,content=self.h.request(self.root_url+self.query_root+domain)
                    if not content:
                        return None
                    else:
                        resources = json.loads(content)
                        resources = resources["results"]
                        for resObj in resources:
                            r = resObj['resource']
                            if r.has_key('id') or r.has_key('datasetId'):
                                _data_id = None
                                if r.has_key('id'):
                                    _data_id = r['id']
                                else:
                                    _data_id = r['datasetId']
                                _url = "http://" + domain + "/resource/" + _data_id + ".json"
                                _resp,_content = self.h.request(_url)
                                #print _content
                                [topics,desc]=self._td_info(domain,dataset_id)
                                print str([topics,desc])
                                print self.make_doc(json.loads(_content),desc)
                                if not _content:
                                    break
                                elif len(_content)>0:
                                    _id_stamp = _data_id + '::[' + _url + ']::' 
                                    _line = ''.join(_content.split())
                                    _line = _id_stamp + _line + "\n"
                                    #print _line
                                    if _file is not None:
                                        _file.write(_line)
                            else:
                                logf = file("file.log","a")
                                logf.write(str(r) + "\n")
                                logf.close()
                        if _file is not None:
                            _file.close()
                else:
                    resp,content = self.h.request("http://" + domain + "/resource/" + dataset_id + ".json")
                    #print content
                    [topics,desc]=self._td_info(domain,dataset_id)
                    print str([topics,desc])
                    print self.make_doc(json.loads(content),desc)
                    if _file is not None:
                        _line=''.join(content.split())
                        _file.write(_line)
                        _file.close()
                return content
                    
    def blei_format(self, category=None, raw_doc=None):
        '''
        Check out the readme.txt in the slda folder: https://github.com/chbrown/slda/blob/master/README.md
        
        Data format
            (1) [data] is a file where each line is of the form:

                 [M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]

            where [M] is the number of unique terms in the document, and the
            [count] associated with each term is how many times that term appeared
            in the document. 

            (2) [label] is a file where each line is the corresponding label for [data].
            The labels must be 0, 1, ..., C-1, if we have C classes.
        '''
        return


    def __place_holder(self):
        '''
        Vocabulary --> extracted from the corpus
            words (space delimiters)
            tokens (n-gram)
        Labels --> topic
        '''
        return

    def make_doc(self, raw=[], desc=None):
        '''
        Accepts an array of json docs and creates a corpus file:
        Format::
            a1 a2 ... ak desc a1_v a1_v2 ... a1_vn ... ak_vn

        where {a1,...ak} are the set of attributes (columns)
        and {ak_v1,...,ak_vn} are the set of values associated with attribute the kth attribute
        the desc(description) is appended to the end of corpus
        *Each value is seprated by spaces

        The order is does not matter.  The raw input is converted into a document of words
        that include the words described above.
        '''
        doc = None
        if raw is not None:
            attr_set = Set()
            values = ""
            for doc_i in raw:
                new_attrs=Set(doc_i.keys())
                attr_set = attr_set|new_attrs
                vals =''
                for v in doc_i.values():
                    #ignore non-strings, since we don't really know how to deal with those
                    if isinstance(v,(str,unicode)):
                        vals = vals+" " + v.strip()
                        
                values = values+" " + vals
            if desc is None:
                desc=""
            doc = ' '.join(list(attr_set))
            doc = doc + " "+ desc + values
        return doc

    def _td_info(self, domain, _id):
        topics=[]
        description=""
        if domain is not None and _id is not None:
            resp,content = self.h.request(self.root_url+self.query_root+domain)
            cobj = json.loads(content)
            if cobj.has_key("results"):
                results = cobj['results']
                for r in results:
                    if r.has_key("resource") and r.has_key("classification"):
                        resource = r['resource']
                        _this_id=None
                        if resource.has_key('id'):
                            _this_id = resource['id']
                        elif resource.has_key('datasetId'):
                            _this_id = resource['datasetId']
                        else:
                            break
                        classification = r['classification']
                        if _this_id==_id: 
                            topics = Set()
                            if classification.has_key("categories"):
                                topics = Set(classification["categories"])
                            if classification.has_key("tags"):
                                topics = topics | Set(classification["tags"])
                            topics = list(topics)
                        if resource.has_key("description"):
                            description = resource["description"]
        if len(topics)==0:
            topics.append("None")
        return [topics, description]
        


def main(args):
    fetcher = OpenDataFetcher()
    domain=None
    list_datasets = False
    dataset_id = None
    data_desc = False
    get_data = False
    blei_format = False
    output_file = None
    if(len(args)>0):
        for idx in range(0,len(args)):
            if args[idx]=="--domain" and idx<len(args)-1:
                domain = args[idx+1]
            elif args[idx]=="--list":
                list_datasets = True
            elif args[idx]=="--id" and idx<len(args)-1:
                dataset_id = args[idx+1]
            elif args[idx]=="--description":
                data_desc = True
            elif args[idx]=="--data":
                get_data = True
            elif args[idx]=="--blei":
                blei_format = True
            elif args[idx]=="--output" and idx<len(args)-1:
                output_file = file(os.path.abspath(args[idx+1]), 'a')
        info=fetcher.getInfo(domain, dataset_id, data_desc, get_data,_file=output_file)
        #print info
        if blei_format:
            fetcher.blei_format(info)
    else:
        fetcher.printDomainInfo()

if __name__=="__main__":
    main(sys.argv[1:])
