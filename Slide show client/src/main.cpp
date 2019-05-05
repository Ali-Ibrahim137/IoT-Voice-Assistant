// The MIT License (MIT)
//
// Copyright (c) 2015 THINGER LTD
// Author: alvarolb@gmail.com (Alvaro Luis Bustamante)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#include <stdio.h> 	// standard input and output library
#include <stdlib.h> 	// this includes functions regarding memory allocation
#include <string.h> 	// contains string functions
#include <errno.h> 	//It defines macros for reporting and retrieving error conditions through error codes
#include <time.h>	//contains various functions for manipulating date and time
#include <unistd.h> 	//contains various constants
#include <sys/types.h> 	//contains a number of basic derived types that should be used whenever appropriate
#include <arpa/inet.h> 	// defines in_addr structure
#include <sys/socket.h> // for socket creation
#include <netinet/in.h> //contains constants and structures needed for internet domain addresses



#include "thinger/thinger.h"

using namespace std;

#define SLIDES 4
#define PORT 9995
#define USER_ID             "New_Horizons"
#define DEVICE_ID           "slide"
#define DEVICE_CREDENTIAL   "testing321"
char dataSending [2];
int server_socket = 0, client_socket = 0;
struct sockaddr_in ipOfServer;

void init(){
    server_socket = socket(AF_INET, SOCK_STREAM, 0); // creating socket
    memset(&ipOfServer, '0', sizeof(ipOfServer));
	memset(dataSending, '0', sizeof(dataSending));
	ipOfServer.sin_family = AF_INET;
	ipOfServer.sin_addr.s_addr = htonl(INADDR_ANY);
	ipOfServer.sin_port = htons(PORT);
	bind(server_socket, (struct sockaddr*)&ipOfServer , sizeof(ipOfServer));
	listen(server_socket , 20);
	client_socket = accept(server_socket, (struct sockaddr*)NULL, NULL);
}
int cur_slide = 0;
string toStr(){
	cout<<"cur_slide is "<<cur_slide<<endl;
    if(cur_slide==0)return "00";
    string ret = "";
    int x = cur_slide;
    while(x){
        char c = x%10 + '0';
        ret = c + ret;
        x/=10;
    }
    while(ret.length()!=2)ret = '0' + ret;
    return ret;
}
void send(){
    string str = toStr();
    for(int i=0;i<str.length();i++){
        dataSending[i] = str[i];
    }
    write(client_socket, dataSending, strlen(dataSending));
}
int main(int argc, char *argv[]){
    thinger_device thing(USER_ID, DEVICE_ID, DEVICE_CREDENTIAL);
	init();
    thing["api"] = [](pson& in, pson& out){};
	thing["next"] = []() {
	cout<<"next "<<endl;
        cur_slide = (cur_slide + 1)%SLIDES;
        send();
    };
    thing["previous"] = []() {
        cur_slide = (cur_slide - 1 + SLIDES)%SLIDES;
        send();
    };
    thing["go"] << [](pson& in){
      cur_slide = (int) in["slide number"];
      if(cur_slide>=SLIDES)cur_slide = 0;
      send();
    };
    thing.start();
    return 0;
}

