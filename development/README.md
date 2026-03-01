<br>

## Warning Cases

> [!IMPORTANT]
>
> * **Spike**: a sudden, instantaneous, increase or decrease in a river level's recordings that exists for one or a few timestamps, before returning to the expected, _pre-spike_ levels. Natural causes unlikely.
> * **Jump**: a sudden, instantaneous, increase or decrease in a river level's recordings **that does not return to expected levels**.
> * **Threshold**: The expected maximum limit of a gauge's observed values; anything beyond is unrealistic and indicates an issue.
> * **Flatline**: An unrealistic period of constant values that does not change.
> * **Gap**: Missing data.  In the case of a station with a logger that communicates every 15 minutes, if we observe a gap > 1hour we would be confident there was an instrumentation fault.

<br>

Beware:
* Specific definitions do not exist, i.e., no numerical boundaries that can aid an algorithm.
* An issue might be station or instrument specific

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
