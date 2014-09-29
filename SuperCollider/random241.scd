//TODO: use GrainFM or GrainSin?
(
s.waitForBoot{
  s.makeWindow;
  s.record;
  OSCFunc.trace(true);
  OSCFunc.trace(false);
  //Dictionary for storing timing and related synths
  ~tasks = Dictionary.new();
  //maximum allowed nodes on Server
  ~maximumSynths = 300;
  ~upperFrequency = 16000;
  ~lowerFrequency = 20;
  ~channels = 8; //define channels for panning (2,4,8 allowed)
  ~allowOSC = true;
  ~test = 0;
  // Filter SynthDef for post-processing
  // TODO: use filter only for some Synths (long ones)
  ~filter = SynthDef(\filter, {|in, mix = 0.68, room = 0.54, damp = 0.15, volume = 0.5|
    in = In.ar(0, 2);
    ReplaceOut.ar(0,
      FreeVerb.ar(
        in,
        mix,
        room,
        damp
      ) * volume
    );
  }).play;
  // OSCFunc for putting a task to the Dictionary and playing it
  OSCFunc({
    |msg, time, address, receivingPort|
    var task;
    var synth;
    var release = msg[1].asFloat; //length (in seconds) between this spot and the one before
    var freqIn = msg[3].asFloat; //X-values (frequency)
    var ampIn = msg[2].asFloat; //Y-values (amplitude)
    if(~allowOSC, {
//      ("msg: "++msg++" at port "++receivingPort++" from address "++address).postln;
      //randomized SynthDef to be played
      synth = SynthDef(time.asSymbol, {|out=0, attackTime=0.01|
        var freq = freqIn.linexp(0.0, 1.0, ~lowerFrequency, ~upperFrequency);
        var amplitude = ampIn;
        var releaseTime = release;
        var env = EnvGen.kr(//envelope to automatically release the Synth
          Env.perc(attackTime, releaseTime, amplitude, -4), doneAction:2
        );
        var position = LinLin.kr([freqIn, ampIn].median, 0.0, 1.0, -1.0, 1.0);
 //       ("freq: "++freq++", amplitude: "++amplitude++", position: "++position).postln;
        Out.ar(
          out,
          switch(~channels,
            2, {
              Pan2.ar(// pan using median of freq and amplitude
                Saw.ar(
                  freq, env, SinOsc.ar(//TODO: lower volume for bbb
                    freq, 0, env*0.9
                  );
                ), position
              );
            },
            4,{
              Pan4.ar(
                Saw.ar(
                  freq, env, SinOsc.ar(//TODO: lower volume for bbb
                    freq, 0, env*0.9
                  );
                ),
                freqIn.linlin(0.0, 1.0, -1.0, 1.0),
                ampIn.linlin(0.0, 1.0, -1.0, 1.0),
                0.1
              );
            },
            8,{
              PanAz.ar(
                8,//numChannels
                Saw.ar(
                  freq, env, SinOsc.ar(//TODO: lower volume for bbb
                    freq, 0, env*0.9
                  );
                ),// in
                freqIn.linlin(0.0, 1.0, 0.0, 2.0),// position
                0.1,// level
                release,//width
                0.5 //orientation
              );
            }
          );
          //Pan4 for 4chan with x/y and PanAz
        );
      }).add;
      // Task for each SynthDef
      task = Task.new({
        {
          //play the synth and loop in its own length
          synth.play;
          msg[1].wait;
        }.loop;
      });
      NotificationCenter.notify(task, \stopped);
      NotificationCenter.register(task, \stopped, ~test, {
        ("Task has stopped").postln;
      });
      // Put to Task Dictionary and play task (in a loop)
      ~tasks.add(time.asSymbol -> task);
      ~tasks.at(time.asSymbol).play;
      //if the maximum number of synths is reached, remove the oldest
      if(s.numSynths > ~maximumSynths,{
//        //get all Tasks ordered, remove the oldest
//        ~tasks.atAll(~tasks.order).do({
//          arg item, i;
//          if(i < (~tasks.size.asInt - ~maximumSynths.asInt),{
//            item.stop;
//          });
//        });
        // disable OSC handling for now
        ~allowOSC = false;
        ~tasks.atAll(~tasks.order).do({
          arg item, i;
          item.stop;
        });
        s.stopRecording;
      });
//      ("Number of synths playing: "++s.numSynths.asString).postln;
    });
  }, '/random');

  // OSCFunc for analog inputs to set
  // maximum numbers of synths, FreeVerb setttings
  OSCFunc({
    |msg, time, address, receivingPort|
    ("msg: "++msg++" at port "++receivingPort++" from address "++address).postln;
    switch(msg[1].asSymbol,
      \P9_39, ~filter.set(\mix, msg[2]),
      \P9_40, ~filter.set(\room, msg[2]),
      \P9_41, ~filter.set(\damp, msg[2]),
      \P9_42, ~filter.set(\volume, msg[2]),
    );
  }, '/analog');
};

)
