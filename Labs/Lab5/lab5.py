'''
Network Management - TLEN 5410
Created by Anthony Gagliardi and Sanket Nasre
23 March 2014
Lab 5 - The purpose of this lab is to gain experience with the
python netflow library and apply it to real world
device(s)
'''
from __future__ import division
import math
import flowd
import sys
import operator
from pylab import *

class Top_Hosts(object):
    def counter(self, format, dst, src, octets, dict_count):
        if dst in dict_count:
            dict_count[dst] += octets
        else:
            dict_count[dst] = octets
        if src in dict_count:
            dict_count[dst] += octets
        else:
            dict_count[dst] = octets

        return dict_count
    def create(self, top_hosts):
        total_octets = 0
        percents = list()
        port_list = list()
        for host in top_hosts:
            total_octets += host[1]
        for host_total in top_hosts:
            frac = (host_total[1] / total_octets) * 100
            percents.append(frac)
        for host_port in top_hosts:
            port_list.append(host_port[0])

        figure(1, figsize = (8,8))
        ax = axes()
        pie(percents, labels=port_list, autopct='%1.0f%%')
        savefig('topports.png')


class Top_Remote(object):
    def counter(self, format, ip_dst, ip_src, octets, dict_count):
        if ip_dst in dict_count:
            dict_count[ip_dst] += octets
        else:
            dict_count[ip_dst] = octets
        if ip_src in dict_count:
            dict_count[ip_dst] += octets
        else:
            dict_count[ip_dst] = octets

        return dict_count

    def create(self, top_remotes):
        total_octets = 0
        percents = list()
        site_list = list()
        for host in top_remotes:
            total_octets += host[1]
        for host_total in top_remotes:
            frac = (host_total[1] / total_octets) * 100
            percents.append(frac)
        for host_port in top_remotes:
            site_list.append(host_port[0])

        figure(2, figsize = (8,8))
        ax = axes()
        pie(percents, labels=site_list, autopct='%1.0f%%')
        savefig('topsites.png')


class Log(object):

    def read_file(self, file_name, graph_type):
        dict_count = {}
        call_list = [dict_count]
        log_name = flowd.FlowLog('/usr/local/' + file_name)
        for flow in log_name:
            format = flow.format()
            if isinstance(graph_type, Top_Hosts):
                dst = flow.dst_port
                src = flow.src_port
                octets = flow.octets
                call_list[0] = graph_type.counter(format, dst, src, octets, call_list[0])
            if isinstance(graph_type, Top_Remote):
                ip_dst = flow.dst_addr
                ip_src = flow.src_addr
                octets = flow.octets
                call_list[0] = graph_type.counter(format, ip_dst, ip_src, octets, call_list[0])  
        return call_list[0]

class Octets(object):
    def toptalkers(self, dictionary, graph_type):
        sorted_dict = sorted(dictionary.iteritems(), key = operator.itemgetter(1))
        top_ten = list()
        for i in range(-11, -1):
            top_ten.append(sorted_dict[i])
        graph_type.create(top_ten)
        

def main():
    file_select = raw_input("Enter the NetFlow file to analyze: ")
    log_file = Log()
    th_graph = Top_Hosts()
    tr_graph = Top_Remote()
    oct = Octets()
    dictionary = log_file.read_file(file_select, th_graph)
    oct.toptalkers(dictionary, th_graph)
    dictionary2 = log_file.read_file(file_select, tr_graph)
    oct.toptalkers(dictionary2, tr_graph)

if __name__ == '__main__':
    main()
