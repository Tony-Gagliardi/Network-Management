'''
Network Management - TLEN 5410
Created by Anthony Gagliardi and Sanket Nasre
23 March 2014
Lab 5 - The purpose of this lab is to gain experience with NetFlow data
and determine network information from flow data. 
'''
# allows for true division using '/', as opposed to integer division.
from __future__ import division
import math
import flowd
import sys
import operator
from pylab import *
import matplotlib.pyplot as plt
import int_time

class Top_Hosts(object):
    def counter(self, format, dst, src, octets, dict_count, ip_dst, ip_src):
        '''
        The counter method for the Top_Hosts class is used for counting
        the total number of octets that traveled over a particular port.
        It returns a dictonary that has port numbers as the keys and octet
        counts as the corresponsing values. In order to gain more useful
        information, internal ports have been excluded from the counts.
        '''
        if dst in dict_count:
            dict_count[dst] += octets
        else:
            if ip_dst.startswith('192.168.1') == True:
                pass
            else:
                dict_count[dst] = octets
        if src in dict_count:
            dict_count[src] += octets
        else:
            if ip_src.startswith('192.168.1') == True:
                pass
            else:
                dict_count[src] = octets

        return dict_count

    def create(self, top_hosts):
        '''
        The create method for the Top_Hosts class is used to generate a pie
        chart using pylab. It iterates over the dictionary from the counter
        method several times to create lists that serve as the labels and 
        quantities. 
        '''
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
        '''
        The counter method for the Top_Remotes class is used for counting
        the total number of octets that a particular site consumed.
        It returns a dictonary that has IP Addrreses as the keys and octet
        counts as the corresponsing values. In order to gain more useful
        information, internal hosts have been excluded from the counts.
        '''
        if ip_dst in dict_count:
            dict_count[ip_dst] += octets
        else:
            if ip_dst.startswith('192.168.1') == True:
                pass
            else:
                dict_count[ip_dst] = octets

        if ip_src in dict_count:
            dict_count[ip_src] += octets
        else:
            if ip_src.startswith('192.168.1') == True:
                pass
            else:
                dict_count[ip_src] = octets

        return dict_count

    def create(self, top_remotes):
        '''
        The create method for the Top_Remotes class is used to generate a pie
        chart using pylab. It iterates over the dictionary from the counter
        method several times to create lists that serve as the labels and 
        quantities. 
        '''
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

        figure(2, figsize = (9,9))
        ax = axes()
        pie(percents, labels=site_list, autopct='%1.0f%%')
        savefig('topsites.png')

class Line_Graph(object):
    def counter(self, format, ip_dst, ip_src, octets, dict_count):
        '''
        The counter method for the Line_Graph class is used for counting
        the total number of octets that a internal host consumed.
        It returns a dictonary that has IP Addrreses as the keys and octet
        counts as the corresponsing values. In order to gain more useful
        information, external sites have been excluded from the counts.
        '''
        if ip_dst in dict_count:
            dict_count[ip_dst] += octets
        else:
            if ip_dst.startswith('192.168.1') == True:
                dict_count[ip_dst] = octets
            elif ip_dst.startswith('10.') == True:
                dict_count[ip_dst] = octets
            else:
                pass

        if ip_src in dict_count:
            dict_count[ip_src] += octets
        else:
            if ip_src.startswith('192.168.1') == True:
                dict_count[ip_src] = octets
            elif ip_src.startswith('10.') == True:
                dict_count[ip_src] = octets
            else:
                pass

        return dict_count

    def create(self, top_internal):
        '''
        The create method for the Line_Graph class is used to generate a pie
        chart using pylab. It iterates over the dictionary from the counter
        method several times to create lists that serve as the labels and 
        quantities. 
        '''
        total_octets = 0
        octet_amount = list()
        internal_hosts = list()
        for host in top_internal:
            total_octets += host[1]
        for host_total in top_internal:
            frac = (host_total[1] / total_octets) * 100
            octet_amount.append(frac)
        for host_port in top_internal:
            internal_hosts.append(host_port[0])

        figure(3, figsize = (8,8))
        ax = axes()
        pie(octet_amount, labels = internal_hosts, autopct = '%1.0f%%')
        savefig('internal.png')

class Time_Graph(object):
    def counter(self, format, octets, time, dict_count):
        '''
        The counter method for the Time_Graph class is used for counting
        the total number of octets that were consumed at a particular time.
        It returns a dictonary that has times as the keys and octet
        counts as the corresponsing values.
        '''
        if time in dict_count:
            dict_count[time] += octets
        else:
            dict_count[time] = octets

        return dict_count

    def create(self, top_time):
        '''
        The create method for the Time_Graph class is used to generate a pie
        chart using pylab. It iterates over the dictionary from the counter
        method several times to create lists that serve as the labels and 
        quantities. 
        '''
        total_octets = 0
        octets_time = list()
        time_slots = list()
        for host in top_time:
            total_octets += host[1]
        for host_total in top_time:
            frac = (host_total[1] / total_octets) * 100
            octets_time.append(frac)
        for host_port in top_time:
            time_slots.append(host_port[0])

        figure(4, figsize = (10,10))
        ax = axes()
        pie(octets_time, labels = time_slots, autopct = '%1.0f%%')
        savefig('time.png')


class Log(object):
    def read_file(self, file_name, graph_type):
        '''
        The read file method extracts useful information from each individual
        flow and sends it to the proper counter method so that the graph
        can be created. Looking back on it now, this is an extremely 
        inefficient implementation because every iteration of the for loop
        invokes the counter method. Our code is incredibly slow because 
        of the way we implemented this.
        '''
        dict_count = {}
        call_list = [dict_count]
        log_name = flowd.FlowLog('/usr/local/' + file_name)
        for flow in log_name:
            format = flow.format()
            if isinstance(graph_type, Top_Hosts):
                dst = flow.dst_port
                src = flow.src_port
                ip_dst = flow.dst_addr
                ip_src = flow.src_addr
                octets = flow.octets
                call_list[0] = graph_type.counter(format, dst, src, octets,
                                 call_list[0], ip_dst, ip_src)
            if isinstance(graph_type, Top_Remote):
                ip_dst = flow.dst_addr
                ip_src = flow.src_addr
                octets = flow.octets
                call_list[0] = graph_type.counter(format, ip_dst, ip_src, octets,
                                 call_list[0])  
            if isinstance(graph_type, Line_Graph):
                ip_dst = flow.dst_addr
                ip_src = flow.src_addr
                octets = flow.octets
                call_list[0] = graph_type.counter(format, ip_dst, ip_src, octets,
                                 call_list[0])
            if isinstance(graph_type, Time_Graph):
                octets = flow.octets
                time = flow.recv_sec
                time = int_time.int_to_time(time)
                call_list[0] = graph_type.counter(format, octets, time, dict_count)


        return call_list[0]

class Octets(object):
    def toptalkers(self, dictionary, graph_type):
        '''
        NOTE: We used the help of stack overflow to solve the problem
        of sorting a dictionary by values, particularly the following
        http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
        The toptalkers method sorts the dictionary by value into a list
        of tuples, which we then use to extract top consumer information
        for each of the graphs.
        '''
        sorted_dict = sorted(dictionary.iteritems(), key = operator.itemgetter(1))
        top_ten = list()
        if isinstance(graph_type, Line_Graph):
            for i in range(-9, -1):
                top_ten.append(sorted_dict[i])
        else:
            for i in range(-11, -1):
                top_ten.append(sorted_dict[i])

        graph_type.create(top_ten)
        

def main():
    '''
    The main function initializes each of our graph objects and then
    invokes the toptalkers method on the corresponding dictionary
    to create each of the graphs. 
    '''
    file_select = raw_input("Enter the NetFlow file to analyze: ")
    log_file = Log()
    th_graph = Top_Hosts()
    tr_graph = Top_Remote()
    ln_graph = Line_Graph()
    tm_graph = Time_Graph()
    oct = Octets()
    dictionary = log_file.read_file(file_select, th_graph)
    oct.toptalkers(dictionary, th_graph)
    dictionary2 = log_file.read_file(file_select, tr_graph)
    oct.toptalkers(dictionary2, tr_graph)
    dictionary3 = log_file.read_file(file_select, ln_graph)
    oct.toptalkers(dictionary3, ln_graph)
    dictionary4 = log_file.read_file(file_select, tm_graph)
    oct.toptalkers(dictionary4, tm_graph)

if __name__ == '__main__':
    main()
