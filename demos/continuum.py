###############################################################################
"""
A la maniere de 'continuum' (Gyorgi Ligeti).  

If you have matplotlib installed it will also show you the envelopes it used
as the random number sieve to generate the output midi file.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.continuum
```
"""


import random
from musx import Score, Note, MidiSeq, MidiFile, jumble, choose, scale
from musx.midi.gm import Harpsichord


def register (sco, rhy, dur, low, high, amp):
    """
    Generates a chromatic scale betwen low and high choosing notes from the
    scale in random.
    """ 
    pat = jumble(scale(low, high-low+1, 1))
    while sco.elapsed < dur:
        keyn = next(pat)
        midi = Note(time=sco.now, dur=rhy, key=keyn, amp=amp)
        sco.add(midi)
        yield rhy

def continuum (sco, rhy, minkeys, maxkeys, seclens):
    """
    Calls register() to create the next section's material and then
    waits until the section is over before creating another section.
    """
    # random pattern of section lengths.
    pat = choose(seclens)
    # iterate all the min and max key numbers 
    for low, high in zip(minkeys, maxkeys):
        # get the section's duration
        secdur = next(pat)
        # sprout the next section
        sco.compose(register(sco, rhy, secdur, low, high, .4))
        # wait till end of section
        yield secdur


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq(ins={0: Harpsichord})
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Lower bound on keynum choices
    minkeys = [60, 59, 58, 57, 56, 55, 54, 53, 52,
                53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                79, 80, 82, 83, 84, 85, 86, 87, 88, 89, 89]
    # Upper bound on keynum choices
    maxkeys = [62, 63, 64, 65, 66, 67, 68, 69, 70, 
                70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                71, 72, 73, 74, 76, 79, 83, 86, 88, 89,
                89, 89, 89, 89, 89, 89, 89, 89, 89, 89, 89]
    # Length of sections
    seclens = [.5, 1, 1.5, 2, 2.5]
    # Speed of rhythm
    rate = .075
    # Create the composition.
    sco.compose(continuum(sco, rate, minkeys, maxkeys, seclens))
    # Write the seqs to a midi file in the current directory.
    file = MidiFile("continuum.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

    # Plot the keynum range of the composition if matplotlib is installed.
    try:
        import matplotlib.pyplot as plt
    except:
        print("Sorry, can't show you the envelopes because matplotlib is not installed.")
    else:
        p1x,p1y = [x for x in range(len(minkeys))], [y for y in minkeys]
        plt.plot(p1x, p1y)
        p2x,p2y = [x for x in range(len(maxkeys))], [y for y in maxkeys]
        plt.plot(p2x, p2y)
        plt.show()
