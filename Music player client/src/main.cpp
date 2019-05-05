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

#include "thinger/thinger.h"
#include <string>
#include "SDL.h"
#include "SDL_mixer.h"
#define USER_ID             "New_Horizons"
#define DEVICE_ID           "music"
#define DEVICE_CREDENTIAL   "qwerty"
using namespace std;
Mix_Music *music = NULL;
int voulme = 64;
bool fst = 1;
bool init(){
    int x =Mix_OpenAudio( 22050, MIX_DEFAULT_FORMAT, 2, 4096 );
    if( x == -1 ){
        return false;
    }
    return true;
}

bool load_files(string str){
    //Load the music
    music = Mix_LoadMUS(str.c_str());

    //If there was a problem loading the music
    if( music == NULL ){
        return false;
    }
    return true;
}
void clean_up(){
    //Free the music
    Mix_FreeMusic( music );
    //Quit SDL_mixer
    Mix_CloseAudio();
    //Quit SDL
    SDL_Quit();
}


int main(int argc, char *argv[]){
    thinger_device thing(USER_ID, DEVICE_ID, DEVICE_CREDENTIAL);

    if(init()==0){
      // cout<<"Wrong in init "<<endl;
      return -9;
    }

    thing["pause"] = []() {
	cout<<"pausing the song "<<endl;
	Mix_PauseMusic();
    };
    thing["stop"] = []() {
	cout<<"stoping the song "<<endl;
	Mix_HaltMusic();
    };
    thing["resume"] = [] (){
	cout<<"resuming the song "<<endl;
      if( Mix_PausedMusic() == 1 ){          //If the music is paused
          //Resume the music
          Mix_ResumeMusic();
      }
    };
    thing["volume"] << [](pson& in){
      voulme = (int) in["v"];
      if(fst == 1){
	voulme = 64;
	fst = 0;
      }
      cout<<"changing the volume to "<<voulme<<endl;
      Mix_VolumeMusic(voulme);
    };
    thing["play"] << [](pson& in){
      string song = in["song"];
	song+=".mp3";
      cout<<"song is "<<song<<endl;
      if(load_files(song)!=0){
        Mix_PlayMusic( music, -1 );
      }
    };

    thing["api"] = [](pson& in, pson& out){};
    thing.start();
    return 0;
}
