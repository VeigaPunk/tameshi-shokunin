# CtlV2Controls — post-data v2 controls

## Verdict

All four controls print `C1_R32V2_PASS=false`: **true**. Embedded allowlist (c): **ho_accept=0/12**.

These are after-the-fact control receipts. They do not fulfill the amendment's before-data timing requirement and do not replace the L1's first full v2 result. The pristine and restored tool also print false; mutation-kill attribution is **inconclusive**, not a killed-mutant claim. Each assigned control nevertheless has the observed negative counter result reported below.

## Evidence

Measurement revision: `24a5a5bb598ae919546715267d76f814efaf8912`. The counter is copied from that revision. Each control has exactly one sandbox commit directly above that revision, changing `tools/tally-audit.py`. No production tool, runner, counter, or held-out file was edited.

Axes kept fixed: pinned inputs, counter behavior except its required identity constant, sandbox isolation, seed, and complete valid held-out set.

- Scratch root: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls`.
- Original v2 counter SHA256: `1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94`.
- Copied v1 import SHA256: `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca`.
- Pinned runner SHA256: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.
- Frozen pristine tool SHA256: `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`.
- Every run used fresh work, `--rev HEAD --seed 1`, default four jobs, and a 180-second outer timeout.
- Every control counter was checked byte-for-byte against the original after substituting only its `TOOL_SHA256` literal. The copied counter's in-tree history path is unchanged.
- Tooling used: Python 3.14.8, bubblewrap 0.13.1, git 2.56.0, existing GNU timeout. No installs or upgrades.
- Probe began `2026-10-23T12:08:05Z` and finished `2026-10-23T12:11:31Z`.
- Per-run stdout, stderr, exit, timing, hashes, exact commands, and commit outputs: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/results.json` and `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/{pristine,a,b,c,d,restored}.{stdout,stderr,exit}`.

### Setup commands

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180s git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30s git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone checkout -q --detach 24a5a5bb598ae919546715267d76f814efaf8912
timeout 960s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/probe.py
```

The clone and checkout commands both exited 0. Python setup extracted the v1/v2 counters, pinned runner, and original tool from the sandbox Git object store. `probe.py` records the baseline and for each control executes the following Git commands with all inherited `GIT_*` variables removed (local author/committer identity set to `CtlV2Controls <ctl-v2-controls@invalid>`):

```sh
timeout 30s git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone checkout -q --detach 24a5a5bb598ae919546715267d76f814efaf8912
# Replace the whole tools/tally-audit.py file with controls/NAME.py, preserving its mode.
timeout 30s git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone add -- tools/tally-audit.py
timeout 30s git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -q -m 'Control NAME: post-data v2 counter receipt'
timeout 30s git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone rev-parse HEAD
```

`NAME` takes the literal values `a`, `b`, `c`, `d`; all these Git commands exited 0. Actual literal commands and outputs are retained in `results.json`.

### Pristine detector

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-pristine.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-pristine --seed 1
```

Observed exit: `1`; elapsed: `29.292` seconds.

```text
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

### Control (a) — Always PASS

- Source: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/controls/a.py` (full exact source below).
- Tool SHA256: `de702e27da95bf79be9580b432d81ebf2a62b995c3d86fdf86c0a476c370c4e0`.
- Sandbox commit: `8c44fc000988f7fbc818e8e576bf006a31f01409`.
- Counter copy SHA256: `52ec3c23cc9d2116c8a723de7d4c901eae409f300867e3f33529d141eee0745a`.
- Expected detector: `C1_R32V2_PASS=false` (counter exit 1).
- Observed exit: `1`; elapsed: `15.82` seconds.

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-a.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-a --seed 1
```

```text
C1_R32V2: v1_kill=0/18 v1_accept=8/8 ho_kill=0/10 ho_accept=12/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=8c44fc000988f7fbc818e8e576bf006a31f01409 C1_R32V2_PASS=false
```

```python
#!/usr/bin/env python3
print('TALLY_AUDIT: PASS')
raise SystemExit(0)
```

### Control (b) — Always FAIL

- Source: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/controls/b.py` (full exact source below).
- Tool SHA256: `9708841d590318a102af2be20aff3a441c3a6f19fa23d21cf6c48bc36c89417e`.
- Sandbox commit: `da4b93b99911f6449f9b5cac0a7bd4e87206c166`.
- Counter copy SHA256: `030dd2d3b05bc7a8565452fee46f47392399f3a80646013a3790cfea46f0b7c5`.
- Expected detector: `C1_R32V2_PASS=false` (counter exit 1).
- Observed exit: `1`; elapsed: `22.792` seconds.

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-b.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-b --seed 1
```

```text
C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=10/10 ho_accept=0/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=da4b93b99911f6449f9b5cac0a7bd4e87206c166 C1_R32V2_PASS=false
```

```python
#!/usr/bin/env python3
print('TALLY_AUDIT: FAIL')
raise SystemExit(1)
```

### Control (c) — Embedded normalized frozen-accept allowlist

- Source: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/controls/c.py` (full exact source below).
- Tool SHA256: `fd6229306a31f3d2308ac2285e86b433dac6242d0a4c801b4ab3b1a8d9120eee`.
- Sandbox commit: `60d392e4e8938c7cfa9bf3edf6bd2e5fb3fbfbed`.
- Counter copy SHA256: `f760117f8ba4e6093418064b2d89513de82491c9f9e83a3bf7f48897e87c29ef`.
- Expected detector: `C1_R32V2_PASS=false` (counter exit 1).
- Observed exit: `1`; elapsed: `19.393` seconds.

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-c.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-c --seed 1
```

```text
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=10/10 ho_accept=0/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=60d392e4e8938c7cfa9bf3edf6bd2e5fb3fbfbed C1_R32V2_PASS=false
```

```python
#!/usr/bin/env python3
import argparse
import base64
import json
import lzma
from pathlib import Path
import re

def normalize(text):
    text = ''.join(line for line in text.splitlines(keepends=True)
                   if not line.lstrip().startswith('#'))
    return re.sub(r'^(  for st in )([^\n]+)(; do)$',
                  lambda match: match[1] + ' '.join(sorted(match[2].split())) + match[3],
                  text, flags=re.M)

# Full normalized v1 frozen_accept bodies, compressed and embedded at build time.
ACCEPT_BODIES = json.loads(lzma.decompress(base64.b85decode(
    '{Wp48S^xk9=GL@E0stWa8~^|S5YJf5=RfsLfL#DBh=+$G{e^<z0(q;l_=&49fe6VLYvQ8A=1lr~^jEbY7}Ah(+bI!)?zq`FN&gdZ'
    'l$UzqUqtHOpg!a33LyFqg`S~7iMS@%^}+qrOqS$;ScdPyNy>Yd?!CEtz3}SL{?rp#9dcB?JZ~rHO`(?;c6QPT|BUHv_r)Xx1-T*&'
    'sRjAiaIwi)bypvaPQzAidhA_FE2U|$c$2?b(va}4t%@Q;QyLEP1?>I(=0wp#vYOvqpc&P7;zgnEow#V%p+5Heypso+56Z4S@Ljpx'
    '3gAlyM*kBPD;I2aPbk9{_>Ddv9nJkW1!t`B!a{Stb$c6uGl}263s4YYd5JFQc95TR3;CT2!<1DiP>+DCtK}unm5GQt_se>XIDRJy'
    '96l^kS5py#NpS_XpI47j=6ja*+_)n_{Pc@Cy~k`)8H8+Yj0%_XbgblnW(%C{kqfWdQ$@=Kqaf6pso%_d9=>r6GqQ&GvoN53zu@3*'
    'OoP&{S$|J)?&`5}D#pE7x^f!kkt*n3RSMLoXt`i24nioOcjarHuBizNl`SO)txx7+3p%Rn;Hq@`8Xu{^ZTEUD9UVTp`1_zNJRL2I'
    'NQ0$^J0Nt?k7I>T9e($vco8YN_Tg_aEtm=lRd9c!WA=ZOb_APQmfLgj%zdb66{Hp~>7o={W2#y&!!9`9Ppw`8PA9R#SO(3=0;fc2'
    'x8Up4i5wG=vR@>cu5MXY#KpGUkZ?%xTTz8l;slJ1@{`~U-*7zd+`c`Ps*kEyc`8G>!QHCZtw%?vnkW2@;jCn$8dRdeLKX59@5Sj~'
    'H=yn5HGE5rKz_F6u?)$$JhWh?l>4@}q;Rqdms))#=Y#RZ=-x6WZo3IC^{+}fr0%%DYuMGP`agY2G4jBH)jt4NZ#<Tkhp>!eg2n#q'
    'p~dbeVTPVuJoJVsKfIbN_5VZ^2<iCo<&)Yu<JCTZZKofo*)8EtVqeN{yVH&w%k>g4$ox2`o*+2OaS>7N3kO9665f2d{YlhfYBtMe'
    '1XKq%)EoZT;{aeiIqK?#wI)QQGv3Ys<^2UURSA*dN|o?ba^cR;a4c^Wjyq3{xTVAIdG7FCg#O3Do;rhM18~w6N|$w^@EsoB+}Ydr'
    '=7NfiH`4P_9kLiJhC*J0xxG-Yv?o6}5;_v7a~x}UoUH%NMz&tBj7<<yU5@giLuK>?Hyu<_Q4+6q-DF>YPi8ztmyN(}=iXg=d~%(t'
    '>m~G6s>E1yDvTY6OtFDHq=<gmI|{?^D~ljy|5)3Dw04_5^w1i2QGE^YhxdeJ5(001j2*)ZaY7Q=Doj}TO`qkC>y{!%)#d(1LKg5='
    'f{$GL)@FhiYJ7v1H4Rb-^Qq&!P6uXbx46AW{<xmj`-OOVk$QXDP7H@5^3%kp9;-Y}XP^PNT9KKe)p@Dsc3f0;i34Asn=J6p4IN|M'
    'n_k}JRxT!ALFPUZ?COy)ieYx#Ta{ibGj7dJ_AD*2%#<q`Op5;{1TCE?`1;u6ncWC9bWzgdOEkV4e-P6!a@*?L0QsuS(#F$InH&mW'
    '=KQ<ZFDHu=TUL%<*iT)yFY=!4lazq-<;81Lv-bA-4;}G}Sf>bl)Z6EJ^8*R$Mh?IoV#8ZI-v51F{zlFN(H@~JAi|W`DCYKU7~m*9'
    'MIPfqOH&epWNRm3Kk21hf@JTb<V>Dw#EnyDK9jQ-gHZYG!XqyR=Z`hSmVB9GuBFs}LWi~Lrcpc&(ke+*V{8697tLa*KM}V6nAs?j'
    'y$iBJ1_Y;osZmQPvs8jJ*JyAXDV)WVm4AZtK@JKEtjA(i?eCr4<ucVxYC%96vYbX2OQz+ztXGal&t2hz)K5|!Prvh8G2f@m?neWe'
    'LZvwP4Y9Bh#fJ+FN9epd`HII;X6N#uYhs@^wipWs2izDx3M%-trfk#zZJHZDMiSx>w8;OSj+9N(wU8pMj=#ujfAac*sZUvG0Vn(V'
    'ztIjO;nBhGNyrs4i*$ZUp4h_?&KNXya)6M0^UBea(KQil!esg>oVJmVKB6!l$?_$MG*6PY6)56}49t})=9p$~OP*3~cF8<0;Q*bS'
    'pWwFdvJf0C2-?FW;qkZZ;hdP*3v79=a6Kk$({?eV@;GX+t7l!M$<U!ubo+{8eXese2o#qEKRbl8G*E&-eFW5C{dZrYJ8<@Z;-!Le'
    '33D~+%6H$nLr)jS63gC%$ju)n9m$3q`MfGRbISavrvp7u8*+#$WnRJzZGzG`!I9jJn>a7X|NJ++SK?k?P1(s)$VjooL))6mdaa$H'
    '_7*q~xP=;wR#V#Rmm+>lju+-F2(945An~vCtHX8SAQRXBHs^ao`@}rc#2Ux3?i0@@+6Ne&6k9|Lqp#pZxV`iBLLHgo_8NtiNkelx'
    '9x7ANXInN2v!FZkO1nvg&!&(+4|pPXV-TXd@1KX3X&giQQueI$!J|agB~pEp>2AIJLOFN%U=mOTU_o&MK{fWQ2N|XidYt^n^-RJp'
    '`=FGPjn*-bC@^SflC0Vc%}~(498`1GcjSE8owI_Oufk;SMHrF-S@eGfXk+8X?P*Pyv-^J1UFGdkwpU%N2c5tqh+dR`iwXfIa-5XI'
    'PK%ODjGm@Ym}@4xm>hdSe`eHh$D}~J>$p{g3G3ii1qG<ya+?~#8%5-Uo3#gZoI8}U#u@9$$#QMK9*7uRw?~V5^7#zABG>&~6%W$I'
    'd-d!!?DVj&)fJNTjD>@TK{&iGptGT52d5m%<)Ywknp_aWO9E5(t<33tx8p;PjI`UCUu2?0(p}`ZF=q`K_jcCp{zAD)k)1~J#y5wW'
    'KP8oml=!I3yeLV<kV?%`-c1YXzT2Wo7=|3MUY{BbL95$<@mHJ`495#mUvkr4X0;o((f&rJnP0WBNQ}muLZE{w!E#ZDv@xmdi#V*s'
    'YE~|)(|9NZPW=QX^1mN$k*IPv=!3}peTxiLPF+yT7Ls_zJnUu;u5VK68H&w<WR>oIBlh2$$)1px<hb;Hl}QDSG`1f(=$VMJ-Uv!!'
    '+9yr{J97bb)9O>WRX;eKNHSz+4IGpD4g*5Nf{-kHl;_3Rn}(L1Md$Q2Y%?s7Im~?(S1-WHbeLtc!DieCL0?G3xQ|q*t5^2-t4blo'
    '93~|UeVv4o&;w7R0E@O6i}+i<$Sx*?eZ~}=sf9gb8vI}`)&kYu`M%=j%?2#_<GI6$tYHRXinnJ9)U)0qtnT)9v`JnnIQ9*q5^v+5'
    'h!xNm$d}A8X38jvIhXoH>zFjYNl;O<7qfx7@X0DAssVO7tyGbl*+_MKmlZm;1KF<%y+56O4Dz>0;%NlNnG}eP>22gank>$+BEkNS'
    '(%*!t+J~nZx`pZC4*%0{ocYnZf3j9$BvWz3x5DQg9^h;8D9&f;_2Ynh?AzvOqeYXN$4<ld&u&Us*}PPkXQOuaku>5z@O3~m168bX'
    '_-{`Q<=e>5K&B1|ixW+d`Pw&Ij+|cDfsVv!mRGdp?NO3|Oii<gTx=dUr%E@`DMJ2^0Cl$dY!27KAmBNb-8Yj;EkZXVY#!j&f_`cX'
    '=ZL`rMdI=F*YuW2c<(3?Lijs#4M6xo`RbQN5!XCA_S&M~6`JdbK`wwj1~UPvg%Qhe@n?g9RUgxg-(rfuIZTSB5dkwUR5FY1GAaUH'
    '&kc!vQ3UHau2)4#_HE8Y<OLccZqDvt*3qMSWLSG5tl?!&#6ebN7u8wbOq!yF?R47V(}ead);8x1<``;@w{TyybuSK00mHPJk#e{7'
    'B`KG9R`46O10Lz;F-qqXvM;Dq?YeahD@T)S+W0Iw$JF2DTm8ygIE^{ENn0Te>sPhC$b4>?V`dkED~ql}OEB9z6-Ys2q+}uz5`C<;'
    'YC?y2*$64>k>BSDt}%N|Iv%}EhkRA0lGM^6BHM=D;KI>iK$52Aht~*PI=G9!*!hu(Sag^D8&<1WuwnQTqxk}OpS3T3UrPH683EG%'
    'ObHG-V9&9~`0#@hKL>c+8+kSMzO?M-hB(NTL7p;HR>iDrd8%M`d4>n9Z_GHTgf@{bgm)ObEyOgg;g>z2L<sWPgftd3z(Js0V(-f9'
    'HL++ziEALs_mcH6nm50cLg5@%_qa;#Id3o@nrQ$G`R<e3F~D>fiSDHg6M2GVH9}(<vfw+#UVa@_R)je{O`{cj-DQ~R^>r$a2z!Uo'
    '0I(lEMQrrL2=4fe{SgcDjT&HUnPuf5pyBg*ro?8D-Z}`Y?=N%e=Q2xA0&J-bc_hIko0d%IeHc4NYZ8CILGBs@Jhxk^IrlRa41CGo'
    'e(a3i(&C>kMrhQAc#tik49cBYKk1{`46#-7oRLeJ9)0#ifRCfR)JPz@kJY6@0pVf@CP};G6DUb(aWb;y1e8sc$NhZYlY>A(g+9c0'
    'K0uHSrgMoqTj-qgv=XR<9x<RMALbJ=^1y5PBMv@I!FPL}@ZC1yu1!-d9(dT>0@T!B3DnwF%isuEr?Mdsi8GhM=EQ0OGs<2(3Mw|H'
    'eeXMw5XThS5G9+I3JNW2Tp(B|n{NN!F0UBxlU5r&-xw_32NwlQGU=a>BDQ=o7N~_esFe|bk}7W;Fz)pUe0)atgE>|r>DSdhN{@Z*'
    '_17hj{H!#%W`FEGH-!ELP7IxxP??(VpEXwHS^r<|D*xdXOx-r?2QP`Ck(?K?Ut4G7Bzi#T7N6-?l<iD~&$wz*&tbZAin6Ak=T9hk'
    '+!*)0-Go1oMCKt&>t97hb>>VCk1#m`KB>46NJkSsS)+s<I+e00+ra_~WiJor`UV==y*S$U-`6I?uQ5q?S&6@t-h*nH`7((3?T2E>'
    '(5^c4F!LbPGLq&d@l5`4!Y+E=9xJo@SDj6oT9;<+dYcFJmxVxGmecH<dJEc+<I~VoZmx-=reZZhyr^jRZK3KRn*~cN6LwAnGBQnD'
    'X$h-32-ICfP=sCF_zWH%*>OQJ+k|RDFdw@TPX>n0dEPbE&I0$33^&>S#$it=61_8`3q%#1e=!E_kF5&2?^0=%#;sgg#SfRbtt|FI'
    'arD?`&P@6ZM4D9@yy?H61LkOR;Ca0Sgw`K+qtDch)YwYeKjf93V7)nf8HtpbD**J+-?Rqk9|^m{ZLli$)Nk$SY^G(IDYB)Z&5Ud('
    '3$S+$$4&yQEFb@Klqvl17+^9N=s@+hoaUX4Usl%N9Pj(x;D&_utAt@pM4y2Wht?p&?op45jvuWaAfTACrqKG@qj@`JaL#BPeW%5c'
    'k$b!@8?+2(D4h58)-Kq}3z_;J#}eJzJ-UpxX8qLS+M!0<iY%X)c%e8J*nPuBJ}&?kMfikiXpM;%wq<*^P!vf?-|gJg@8dAm%JNGh'
    '*s7tdLLSU6?6}<Y5m1&n_z<_QdA;)Twaxz_i-@eU7*f~&ED%94iwh=j%1}aFMgh|VO0DW<f9|RNZ)}B`!q!gB>=9UxmD?f;<<CGd'
    '+{4Ci+~iSK5K}fXyHBLCmFeaEe^p2VR1TzTk&w4RjerE#5r6zQNJZfH5Q73}EaBMnl=c$u@&%~6<|mS)5_J~1CbRarbD(*>^hTPT'
    'UjUDKvUkxLg!pRw)Yw3L4tT65<4JxK@ykm;q;U+v!nw1gUHK4ICJLMjQv_?}flDY`P6tvzqsuoZ-L0VJbF=xsR55^3S6q{X>JQGL'
    '=KKe&nura>awR{<A&?~bx&*n5Lpg%ipg9puqxl)~ooYg5?G+7+5zkq?+meq2g9<}W^pEM*q$*7A=iCiKt^*oKkZA25910v@<m#wI'
    'A)aRAynFq5jEH`4VH8I>El}!meT|(EH}u(U&Afvr_X-3FO$|MtGPH@~@9O(6xk@bsR9reBu&R1Z3f?X$dsERvp5f9;rmkq_9AF|k'
    '#4hos?MLqhuU!c-o1u<R+14KYD`?<HXC2g^(vp>RvUgspPX%=jE6{9AEAwpzLDz1Bimktx?Ah^EKuxMSVqy0Cu)t*#{(Xe1HYfr{'
    'v|n-h;Vi*Wr}}}JN<wg<`V!U$ZeLmVdaN}JzKVz);zys}5mndjU!N$rM<q0+(%?v-REqWGp3_0Th4?g&3G={3CT(R<8`vJr!AT28'
    'i7zoDU8f%w7!ACI8K)OEI*i7aw#L>7qhtpcxm!KI@O5T+tm7r>bwP!(!Wq0sHhuy|_v;YE|GxG0>pj3lhk+(1aGS&yWsR}J1djVJ'
    ')eXS6_{dPo&DW@Vge+XFuK&oBok}NFK&Z;CWYU#6I7hyd$3>`Rxom2`+N4oq2xx~zBBUFpJ_PK5Ja`febFJBN2M#6@hi8B-FItGG'
    '`?wNDlJ&p2{W3tQ@VYnqYQRNEvhE3n44f=DoutZ%mQTPpHbO&cyYE@Vf>Dor)-U>{AD=t{-dmchBliY?It)3@mWPSI<TBvZ$k`bl'
    'WFjt*78L@@Ckzo<=n0aNag-9!V+(va4d8o;ol=+u2AW46)<0U|P|I7p>9i;OzNk?m(GadSjaTb5$;FHccZw?{pOcg_48LeNtUz25'
    'f^?ci_0vdIo;ly-*$>=JT?H=<YYV<N?!|1p^sc;|pIkj{Sd&(;k{-T}BS2W~NI+Lj>RQsgmv-@qtS2x#Cu9S%7iMRSoN6flQBbfL'
    'qvhMWKx>xw(|sbYC3Tl8C6+=Js%~%pMkrT7Qkcne+tOkw82~@1huhPRx)Qlv=6UA3=!3Ym91242>$0|)fcKdCLtW{E-G7RkK5YL2'
    'F^a59Eh~YH?DiBwlThZ0YC>IKmokut4cfaNI&ltZaF>{a5d7w7Ajb40y8hHdcy{c$I7{YVQyXG{SU+GjkgTB}Ck^2vTCuQ#?E#NC'
    '=Gc!RT52c+4daB8H?0M3s!JX1lTJEp`h$Vf4^1=nFqttvJXz=^u?%_N7M0WdHTUzP^YcW}p2*PI%?sGw)2rb(OrB(U3rLR-2t39&'
    'vCP$HO1Au=$o_3TQf>j=uGG|x-(?=hu<NoMvk+1(Q$$RFqf)hvayyI7HX8&+aEWekbR`bQ>2&a1N|aRpSfI{5!xQ#1lqyM!0W1?S'
    '84@+e_&EQ=IkL;3OX1o8eh%Q#)~NkQ`&t-;6IZb77ggG^=x1b_)Hq#IYKi^w16M>vS6fYk$wq*#*D&k@;lW%*Kv6&k5#ttzJ?KYa'
    '$SFX&3BLX(P2yi#7X?DjvJ&zaXzY!$XtB}F!Ut2Z5eOcwH8hvxM~%pEZ~4*a`QPnLV<j8cV?{&!kIzLik3-5{s(fC|UKK4k8Q|}2'
    'U2&O^;tc4+U6Qd8eX#Kz0#~utGkY@0vyi3{9AS}a<A+Z*xlNzK{4Ggdhoc`72}pd31dV@c7R!pz&;%cw^gdd+D9&@w;m-rX*h5Tx'
    'Qsx~`gw0{F-|hYZ^LB#a=h&&cPhE_p`GFg>DD3&NOU?jvx{5JSVm4OSYxW`IM@_|PLTs5E44eJgc$GU#@l<S(Lw^)DLlIE0V^Y3i'
    '=c=($u)9f#Iag#w9C>AYug{DI5W^^)tr-pOiJ(TtFc3!Z5}=gK4|4Zqc;ZvHGAE&=(dUwj<xNyrY$(In0r&lr^3$`V$Abet)n6&8'
    'uB)BB0NkS~^S*m$|D^`j9H>7gbpbbs)P+KEMpeClp1>+5R;!P9u8tG%_ZS3$&S#C-z@6EyN!Nyp6&;;hw*YDmMG8{UXyj`k<hH&_'
    'YL>*WkiGk9W+*}9mre8k*c)SSrn8HYAC%|vt0RWz&|8--&K%wQ^_-&FX-{m#Rr78%VaUCxEuALEGTUX0n1Q<wKnr_SbM2g^R7zdL'
    'jW;K`QzUO|h3_hP{svof`__o~QVJ^F%(D>+gEVaf*OQegC6uUtWL{;ec{MW}3hjPq0?nSkB;@fW1z9N_=eVCSHct}xr>l1!QG)_+'
    'MlpYP`lUz9z@;1f-+FV+Hkyz>BQLhw%Q<LvpmeRhtk`_JMqFUK53G(S-a-=_6%;0|UY$;o;?wGsObnO}mr&lY2PrIjxvtUkP)FwB'
    '^c&P$H!j<^<Q_t|^lqNF;VLvlrM{t&6v%CAMUH&fmBvjH>G7|5AS?-Q@iVQm?kK-U(n|DCqWVCG@qzcJYfYBn6!;G%No4ntg^K0w'
    '`gZ(}Png+oOj5`eRCDTi817T`vAwXptsmLk39bM(*~L%vDwwO8B{?CyK(o&&CDD+whwnf~t&tFA1y#xOgGz_6uWWBcxL%!(|L<35'
    '<KwyBmL6WeTy!Ev#%lqR2VVF}WoD$+629ieDc~;KRY~I2^GjD)hL2o%|Ihm|o|4Wy+(TALq~i$dheY;p8?)eOAFC@i{+7WX=qW_K'
    'O$Ln`dZh_0T+3BQP-!tIbcEKe+&!@ZwcmcH1#tTCBTFkM`wiOF1uRe47(=$LYTB}ioLrvjixhj(C;)qe%}HrDK|Ak?`H5h<&wMWH'
    'E&X0GkLC%cvEUli_`ov|eJpZ@oU`($6Gp^K#HL1V3tPmBJF0+?$IV)zGb=B!)a@bLwIZDS^BFEH<9d~=X9^3dG}OEf2Y*DM8<)>%'
    'yOwrkgNomL17&B^gH%Ecby2XN*so94nT*7Ul?hfOUqiBx$+2#!insud$5)NVvn~c9=sc)JnL7=@^@se8&OmD0ZU<*&Ff#UU4gHVe'
    '$6kq;Bc#ufgZc!~(}GW=m;3Xm;B$thEra9!4i+NlgV##=ejAdPQJ34-Kg1%0pzmE9Y3BN_=V(-3wSA~{-FPlsz^$+Z620!|s4~~D'
    '=c~pHUmHjqSp}kaaEhJ_o3?-K<yz_BRe!oXhLL8~^8;|BhS<b6=FN)qM&Si89j^o?q62=X9gk!`mS4hY2;!&*{FKU?r#FWA5%cRt'
    'D1iayzj1idv{ib7`Jq^$UvW&LeEe4Oz9r19vv5-a^fS?Q4F7;JdE5R!Gcl$8l%5GdwG~~Z^MD|z)Z2bp;v04ZCR0OtBgXBu37kgz'
    '`F7gGPiUACNeB%E;MPcxzk&i@+pv?Y+5EeG65Gw41~^cWg(5Sv4h5hN=5TS6pLC((h*5UVNqx!bo}E&G)V=Y+D@XfA)%&UnFNt-Z'
    '{Xrd~TDmP2)wlFof{?JeAzjhK+Kdy7k_=BB1c#8unq|d)%R8fHv}rLUbJxEUGZc^66P$mJ8xw9#w8Z%@;W&qECov>W#l8Aw03+R7'
    'N;om1Ei7<P?EbzlO-MHHO*+q<0BBbuDclX7wu}PlVBJJloWat=__A8=8nK*LX>|DR+pQ41Y0j15+2g^0>fc)m0YRaXY9)3&M1nTT'
    '8}oYoVA(VLBElY5hNZ%%+TD@c%2$PL{9(7k=OozF4MAJlHX)Vgc-!MvQF|su4s_Caums$7)V3}+9NjtXq2qZRm}_A!v(137aXL!6'
    'HcZws?v`6(R<M|xIy*Pyw-X0rqqB9@aHE8RbrLOfx)16`Vta4hNh%V_-y6&Lwk*0Rlv4`;hIPgLsGh0iz6%HySh8eVjS3SIoA`Xt'
    '0uGuU0eMq}DA>gm6H?#fo++=J0&5SpFGF?)lT~;zvwvEtj8T#Kr#bgz+wbyQSv{+G#nFng(ai6QU?mG<BRYrBCrNnXhn(<c%Vs1&'
    'd_4`+pg_W}poOX?lX<wypJlFlFG!jK4s3UA5_em=?nVtpij?eXlT8cx<69oiPpy{Y!C&rTFR2OPHuA@;#?vEk1A|dNAms)~zaqOX'
    'dOKlZ$;s+HrII(ETr@ve@XYGy!)WL}oQ<N%xJGO2fF`}X5d>=U^&t9K>`i<>^9d817^sJZU^pptFtWdL14KQ18|~j#1Zu;U+A)5s'
    '%uMDYzu7(`sa0!5ER1<C_UQeAy?9D)Xf<brSgW&nuaj^vu&}M$7xS96sevpD-+`sN0nit?!LSj_fPvGphYqxu0=20+Z#oj7M!Fsq'
    '8y?UoW1Ore*w?})dD<3t`A#%5Us&)$$)+N)vJpdxs%a8hOwAFk-a+@9dw)m1mYqv3f6=_oerbr0s}cu%^iM*J6(D3wyL;jXsV%>O'
    'o|DNIp6jgp*vrip{LfIAj7y!!Fj%x0H)G)_h)Af_GbkL{M72P=KpS|LFZPKVzxtGgAJp_$kUIG6yJvZ{L&LhoKX+?6CYEk?Jv0|6'
    'Y^5jalw*K>VFr8AxpWW(|6K>(JoY6<28Pl*6%o<~*?_h`n?xP(B{9IUb_XUm?r0S}dS})xhMJ}UAo)+AY1)(v#4Ma5XXBLh@%_-<'
    'H2qxHg!K=uKRzIs@-@uzdd@_B?bmJ@asvEr?~+XqLQJo67ruaMXPlnlJP#tlA++?W;u<SR<wNz_4gx$u*{{zu-@Fva?>jckCsLk9'
    '!4m|~O^ptSxgpSDnetZ!oN8K5C356{A<Bww`|-@wsQgWjtTr213q?y^lmJbw+>$wY1wQ1VZQm}HES#W+Uvf0eW2QC4XffBi!Hoo%'
    'z&hr6L&h_o_7mu|?%CzJ60dfPx4X&FV>91ipM;UmyGGKF%;)_<YEyYwWiz2baHQ6;x0>?`nq(euiP(caea;wFKr4q{AEte@_R*-<'
    'T=~#@uNatV6Q#w^zZ_h1Cfi6fUTOLibIoOfuG6#AF>c)KMPJ`}w&YrX;H}9*%EI+YCwzu*Ze|fhHlE=zB!45`!D>(+;I-Wwium-C'
    'HJHm?t`SNPM5T=o5M>b&5q{z97qi|t|1KOJ+LCEYz>X9?TU<jvUUojEM|Hbfx??|Jak(zOeiIX6VP1TLoVf$!Vt174QVQyd^}$xR'
    ')<YDb6`xMGU7`mH*n6(RNMRu(hl;}JaV!2$eOKX%@WM%+qKa<CyUKO?znoeFrBYaW|Nr-lp-T8|v$!5HlDK1c`gzPkQE(cZp(6No'
    'NN~cGhUfWsvr;;Qsm;<_ME%)1uLcoFi<`-%hE$&o5YEi~r<6j_GNU>qP%&IQustGL?_bpcdHT-0)Qf{c7?XL|Y!GcV9FD0o=4>;Z'
    'd2x@|{BD#$vGO<R^lcHzp$G!YhPV6LU#K{DKAG5Xa$fI?WzzMmjIFJ4gYh`;tKVcrW0SvI`5s`=PZ7Pn6&FNEQd8k#4~Sd&Q)Ht3'
    'Ee<`1gLFM%y7`@xs{C6`{#d0H4UkI*=v`ipdkPjrgf_`>f$R<t-Y5<`(qc6CGlUTJj}h(jcQJdAI#V8H>M~ivc9HdnfBtT<K&>EB'
    'p<&-ku<2#82omDu){4yNjY2j0V2LUKOOJME%5V2l3an(WPKizJ_cg}y#b3rE6d)cYCP^FRW3^%-*E^U~5#1p<fo^?h!txM+kbi3o'
    'NOGlcIzG$dwGf5|6iC(P&2~5lpoj10YP<0hy&g8l;G(*?>a}{dRi9JrCiBb_=C(tyBgc|-ZEip7l)+v_RsBP5s;bVuow62*ng<{N'
    '3<e7TT+W6**SCA)I@I}IeE&)R`!>}GH$it-xT67pGM3f)z;6aH$H$?q#M=6uu~ErT1ob>l>mgdkTp3bAFndj(O6*4tbIe>m+9JCv'
    'RMv_1fMw+!@o*dD$HXC<oT4fLfD@V0XVV<C8bTU^)<}}0TvP{#F*WoM2ld`)2)PEZ`FoIL&N>Tb=KQ>_1^G>UYoG<tyUKx#;_G|X'
    'caF+wgu2%<8LV10ZPWeLEk^a27~W#7Z?Kc#J9Q;T?CVvOoPJ|7uHM(DIX>(!*}wiT@txFJY_iMJgv?j~TB^BxnGTKgO=@%mBE$#D'
    '>$Mb1kuz9NWx$yCV9LSD!PJzfkl)!S(-A!oSv(-^up|2Hf41`#3w|Pp*^l-G(6|fB6Y_j+SJFl>K43?dwXn@t9B@72M5tqxI|#ws'
    '_&J^TYcziod=7cEj?DR|6uYY%p(PFUyhn^&+B}|(>>g4R8V^_uywGno4d<Q5E_431NvQSms1+t~sFK9}F!t2w!887Z_d&k~s)muj'
    'P=6Y4e`68g*gqK<ei)wSOa-p-Wa<g8o_`b>7VkE_7?zq`*R1i2f;q!Yr-#?dCewADG3bH@&*<Xk*yp+(U#KA#dbeH$*wYV!ht2eI'
    'H$psqOai@p`<LZH&8F>i_6ymVVOhjWuB(=87>p96ODANYTP6fFS-;3~()oV@zJf_>i-u>lS$E}>#0xsZXq}_$^UlAjX%~8SVp(FC'
    '#cnN%P?Ssh-$c^wMNl}4&0rdY%{oL3Cy_b>tLrpAYA<IpN&Po1+daC~^D?9(a}4Uxqm8RzDG6yQ_TUEqKtotNUaa~{gM}8)SOy=S'
    'el%m&K!)juFnJ5LXj7DqkXi1>lYJLc9EEe)2&}hl6zdgWCLf?^cz-soNpD20bZFzGU~l0RKoalo6!kP=LtkQ~(rafuR-F&e-PJ{A'
    '$7riAlSBk4l^1Aj!RR{|vk4@S>qKA140;iT`)OM0bKC5nF_T>(hPhdRk0*Zu*fH6HLmjF}5>WaXK5+$PhK*yrRanhpxq<_BJ0%gB'
    'q;V$pV?u$EA6J%cNzI+R=mDqU?B)zM7DTa~nCL`pECQ^EQNZ%g^z_xD%b{m&k>@FTFIpWY3tH7OjDz><y5Pbq?}ATtiM?O2Q4QsX'
    'j#NbqSIr|WOqYU2?zE3YWDB&Km>gYvGv>|m-bBUu9i_5@MdbS!(rd-p@Mid#Z1Y}S<NL+&d8|oRF6b;3ccnIR&!&bC$uD9|k5zpd'
    '`Nk<6(=i&FEX(>y0PUTaI`WJvR{Ep+2093V*<FHefY?Im2a}(ff%nT5*4^mQ-@B)f$o+Y}r}YB8cn?Y=b$2j6Fcs=_Cp7&qDG-`J'
    '*b5stWcJhQuM=lW(dZB$x-OZHy;I-4N<tYxX0~fx_gEqr%1)V7h`1XW7$e|%`lsH9r_#B)A{`3*&jJ;l>)iAA7XsRf;x}fFI*?sO'
    '*qZL<?)>9f-<w%-wnc#We%Ux+^3h9IX!1)?WNw8Qn$@<IH~c>8p=P4$KD~9jubKx?q4Xg6(&)h>>+)=w&l({OzO+KAS3|t;`Nd7M'
    '{aYV4PrI9)wQF5}9y<Ugj5dL#)fm5<v~R^OE5z`X?|n_0D6bq_XXtxGE%_;?zQ(xqXkB8riE-ag;$P0Bs`OX$jetUyPwM*Ng{6W8'
    'GXI<#ww66KE_LO`>r$pzp>bUG;3^E!?h0o6hLj`C^(Od<^$G@!j_6atwOfZ5&P`b3Uk-DXxD^~VzyEB$OLPy9LeMZa7R24}+@>aR'
    'ep02EpNT}N1;erwluG$tI$-($5!$~-Z=RX7$rFvI|1eDDDUtUtf3kW12UFpidi|>k>o#<4>nwECS>3LOvuV!|;(3sgAM_B2c6rqa'
    'g(Rzw*oLzA;~(q-*U{^`h${8{V3?4z=<1ZCDx1g76xgWIj$XFsw=jtG&oXN}=1O?5RZ}ilSGwkPF+)J#i)_RU_*Do*Bt<mtvGZ21'
    'w&IvKf@__RsS_KdJGSUT#AW85Q`sKw8@pIFIo?*8Y!%#umc_p7KHPIv%zBB`5yg^s0oU?p#v+$Jk+mpgy=3^0NhQ_`6VZm7X9qsc'
    '1k)fi_xoc)z1`JJulzi}R~XEXtx4jkv|t#tvPS^>?q(sbPRY?OAk=R~q;Tqsx*QF1`O`9R`TrIZ?!^Xh-C4*0n^v}M9HrzA$uJ+='
    'kMcQ#qA66xxF?>M_NXxvV^Pm<5w&Je**d_4zbcKsy83d-h_G}8<R5XcYg;<L!Fgon?nN5%AF&pP<Ah{Y)9WRLF`)BgmDR4Yy$36X'
    '3}DFt_9(KV!LaCR3S{82B)78zxhelCH|<`z?)MWWzLUsh?s=7?U0w~ai01Y_{R)Z6%GzC%;+|<$Gqr0;IuLFryFk)-x3ru*BCkRU'
    '^Udhm3uWFmOLGwNsHmrRY7gUf4(-tTpG7h2uP5V))@@f$kxlaZwDVz0E7HHST33%)Fjt{;a`AFz3^Cnp9ueNF{a)4!3iOz<G1qTG'
    '^$nueY{L&>W)HNYEjC8-q5{{579y<o4Gm+xZ4keM?>h@jo*zkjwBSg>L}{B99X`d~MDQ=xx)|}O|E?lhMnqjX^WY>O2B2KRWhKf~'
    'NHn;@Rrw7KX90l1C~$-pUe~BP>Zx@fk*{;Lt41_-(Yhn&4cthThIE0)BH;oeTepFSTh$0FAz+m_EO}gnSbZP{E)_W=3Vpa?zFkNr'
    'fM>SYmy-n!I;$^G)3QqWJf1>~_n5>^LdKH&9R@W9-HuOB0f|#seOzHj;w4i(`MVU}&Syq><Yc!HeBrXoo~qo$^FeOJI0jui0j0<^'
    'q31{~ScthFN3A@~=ZVx!XnkRdaqu*DU6nW%^H=QNL{t6{2LYgITpT=RIUG%_(pGoAn;S$m#Cv!#EdHORz(071{3Es<o)z<zkHm?+'
    'Z>Nh7+g9e5D#Jes(rs!}&YF2rN<f!)op%BQ(RyY%zEOp(IBsEUWg$dS?x!_0%b6ut7J9BpcY$9cG3UxBcp{-51(CAW_2<+*p<L+~'
    'B*sRIL<i+3(TY&cXwUlsm|yff^;5^Ki-1EXd1eYI<Lw|jO&yH2s4|fXg2LlqGze&H9qDWED37!2OQj$eXmG$zsxUwCz?2>jHbP4d'
    'hBpnrjRFW?P3dMv0Q-y&5siY{V_Y^{WNvS;r)$yIb>B=sot}e`@TYN{uajy{hni>1#)K*fh~6ZwhaJ4zsR@cs8Jm!KO<s{<k}nPu'
    'D5=r!{4g+&b`qN^M6R&ils5R<a5+d=$uLIzZefb5kgQN{61oM6LP0%gBm_{<#zgY1Kq=gJq0>rEl1PFYcC@?feeK<r7+N!ci(j|&'
    '9kmF7ssQ!y{0S_Uz13V1S!)`s9RprqU2EI=tjz|uS|%{2z_^y^F|xSHRC`BlB)Y;%9rzxMti_R$dnsh<FNBzq^%4AS6CNsySOQsp'
    'gLoOo>KzT*e06DZ+Tc`G1I$TYWk2(d4=-6s2utPvF*>==jY)xQ*xdZ#+$&$TGaz$|x$-n*Cp0}WM?XH!1P<iLEKH+ek$h7?s4o8x'
    'g=ctK6cH@~mLn9hz-?%ur>9`~Y8jbCFC-RBsRD#0E;kIJDQ-<{K^f^UAmCrj#D;I}WkmeoRc<A&jT=u#LMd~Nnj?c`WfguAFQkS@'
    'uU-1a*#Xa_^=$U5tQmcwcMrw?^oWuQkvCmQuR&>BKNA!|)MLe;)<wSOmg&&8Ug{{l8(ftUJgpM4)oODkbYJ6XD}j2Vt@<K5az_h`'
    'r5*>Cc1-dD!(tcubFp<{bWUx;W^V3{_zpGMqlQiX1{q)^@LMjVedij^{_^F%N^$Dn>9*~?h%=59j}cogr`G8c*Jw<#Q+zbKvdTEM'
    'o1?^&fihD*w`AeO2XdyMhk?#vksdec<&Cec%%@lq10j4zFJ#5V86!A;mEOSYx{;rTyP`&z2T&<w3>;fAUh1K6FMJyAMth09^gb8b'
    '?@JV#aI@PRkht!X%3}bY6#n+-VdZZ(1eT7D%T(jcCpYEsG;vukbuo^-k%jaoY(zCjA2sbC?;elxs7DP)Xc2_77SNHEA>}=&oP8H&'
    'r+Y#R=}386@K62-0VcV>`&weR#yraH2|?~d0V)UsUsUBh$u57<K<|q01xA8SLMH&pu1CU!atSSJ!%FOCZ#oNmy;QuvO8UZcOz}gB'
    'I@-d8ZedScAJ8Kf>}>4?g4qp^u3ygCYml%r58}q&RQiTdNwIVFB!hllv6y*2fZbcsTj}8q5+ycYQ)UJ-0;&1yqzMiA2ADqmR1eIX'
    'C&^8Q?;2~Au@shiFy@E1t3(#55H5MpNs|~g_5i^3rm+Ecj#)7@2>0~IO~$``Yjqs2t2g49d@;c1twv?e#`d|y4A=v6hGCzGU{)9='
    'GOGyppknLw7EVQM%uLFC7mkb@Ee~19o0Xc8Xq0sC;Dp<!nKz$|&wXs-vya2|ssWY;n~hQI)0dhM?2f?>8974l_56}Jb5BZq(ZTxC'
    '0)gocOQK#y$})`_eBz))!|6Do*iCTrrxGJ&xrq`zTK=F3n5(f&+bylWFL!xZ_27-zX#;$ze=)V4IojXS|9*QUI`c`6rSR*;4d%j}'
    'xy5Mhl>Gv)MIo_QFD8dDKYfLJj}*sdEbLK2lMruMcFXY+?d7=CQ!Y<Zc%+WwkNo}hT`E}nP_$F!Q8*<}#lRfIxCu9*@_>yMu|Gj('
    'iFmyV#`Gwxaz0OD%`km!_>Z=m-Gqb^5|YC;`mELog!WZC7Iy8gD&%1!TJv<0=m53Pw?!12!JJ-VrxRF}2|LskpJC|IHZ{~|Gn(@x'
    'zvr2P75fz7Gi~h6xee#U*>*x=AQl-+qaF!kg8S5dN9W>DSWX46mkTJA`k}ZG^(LsmFG-jSadK6_jm2;J+yiBE_r;;MRRSlP)6Wfd'
    ';xqy(%2~m3G(RlkE#QYQ+B^NYwNBaWg%5pVpK%3{Bwj7ZE{$nB&+WFA3@yiW`3V9swM~-x?;<Y<o(XUHlg|7Py9SYbBdIF5`>r7o'
    ';6u@7LUmNR3!Cc}pTF*Hf4s2;+2{shaizoJ+U;I2)%1=M79&YZ7|r)<#kL6taJ}iW;8Ucb5$y$0=#tj9m@Tc*F_^UZ%7#sQf~1KL'
    'qPP^nYz>dTn`v-g;G!9gW_piHa%o7QMRl4<EaXQSv?pr&eee3XLciIIb?Rt{cdSUBq@JELq+*sx_7ZGU^NRfXxdv^}i2!T3@&hMh'
    'WqF@APXgSEqlCyW#YoBVsag^Po}j^lE0)ysup{Cr;lKr#r+fCtPO`zB80jw*>TqY|mc2WH+gjivX>9}8R=O@l-j*r)^_@9XMhPfN'
    ')>2tR2U<#T%7^Pe$ZnzwPw%l2`GArX-H&Fq927+&6UUAUH$Ku?xvbm?iWP1@KP#GqnNa%*-?%68W4~p{!cIe<+I>R9su5qGCFS6O'
    'WFy$Zog+)Uygg!wKi*aOx$4Jg>;)2)bKUv(VUVW$p?$&e)+<Zky-^<Mfs`7~azGA;rIbF~4~BCe*ieN1Za^MJ)>z6s=G=)(?+@{4'
    '8NDYqs8eH>LZye?8%DO5#C}_+kV^3Gh(d=w-;*I4<&U-qkTKE`r}Ht(l0%)PVuZBVyR#?AD-qqe_(>^u689w9L$lGpDqXf2vnX2D'
    'PXBt3Kt2Cc<9e^QgGf95AZ|+Ka6t>!Lisy;41&E?0ZxtMKY#T!ZzD_%Zk9O4P5}D93&Hvfs=N$}%yqJG@t%w8)>-B+5nrJsiSP9U'
    'b+QUxsycIFWm+a<dx-6#8x<-^`aYK;Z(aW>7dP==TdVNd+e^Ba1e8p9*wo;me?ZTgQ5*dD0ZtUc6lE<Ty_o7Bx3SO@Ij2cEW*H#F'
    'lkp*S4R+T4WVN}4hhG@+$E`E2mN=Ryp4aq4n}(D`+wbz*-D?5hf=w1)`w8#82Ffk470}ufb5)gHx`To#sYTinw(Pxuyb>Rr6}O`8'
    'Vnj)h?Zlxc2vuj@pBvNAt?q^%H%}72*)?SnK!W(?B1O|16~W!%Kv93{x`ezG1AZS7Y<|hcG2Y&+0v>np2o<m&e~mNAsyx2hj9(#k'
    '$P8JGPn9;lnZkg5Vb$&5t_h<p@YHF3hK{07V8fXiimjn<`c(D-F%ma0AQZ(#zX-KWSiMD!D85}=IW+4F!xCD#d_FR4hCA9g!D<fu'
    '$BCpw`PspM58{y-#=@4w#*VJkDutW;u+g*I{I~Gr>?n15s#_b+O?WP){%b&3W%Y&etBZrRXVm2;NKOS3P8I)J>Gg!f2f_EMDBAVN'
    'Ct5C4cCk#c?b7W#m55F%!lSt<Z^+K-vSG%?--*mHGzFoxtHDurnvPwH!=+`T!stk^163ag`F^zy7!aEAUOoMU<Zo5b70RNg#b55T'
    'C?tAXh;tCB&i-sNf?SqW_UfKkPM8#qpJd}{h8SrL9Mb598rPBXS`=V(v*b)Kh;%bBldV$Wfz^Hi`3werD)nRk+8>}0|MrGxw!nfH'
    'y8{Ix@frJYB7C-SfHq{|*w~rO@8xF-@#j%|R)xDdG$sMOA;^Nz`SI>l&m0^bg-?bx$>-S%mWt=`Xl`CK5*hIB<V#-LG}y#^=9I4y'
    'C$t0AjdE4BT;~~fYsRF}(Q$&-i`~j3*w!}9bx8U2i#rNfL0s=%u5;qJWHNP3mp!H>Y)|_TAcMD1lCu#sN9d$>L%OvTDo2Sxv37FY'
    '(}3fSm!jq@`#}0?F3=(PIO@8(52od<gEQRkq~q{RE&imC#f(YK^9GuIljap>Vvn)-yeQ>My6!}vJ@&5Ed!cPiO@BH23VS*kbKo=s'
    'h(jd?8E)=47d$1otKNIS5FcpXP(O2_w$13n#TcW2+#*`6dII2rriML%TMjV>4^5BVIIfuBy;1DJ4T{D^>r*8uj5SWsQ1{iG9(q@j'
    'S+~wlshGJX^48rh5qt?PZIAL8<Q^q5Lf6%fn9yYABsSdy1=*zi;M=)x)OMfdgn+N<+(F|NvFp9Fe^L%md?h7chr+$mxvIfZUaZ64'
    'F&5V71-3%nt`;lf_l^Da1sD%8SfsOms4Df@r1dRr$MWv>sqiY=@bmoxG&-Z%vn7oNl&I0zWLKZJy*hbH&fSaCtg1cA<a;nk7Swf6'
    '=MbH7x{0O?E|GvZeJ4_b_vveTZA+%AtI+h@7ciw5dr5JI|47bXF5m8Htcq8f<pSYDx+MHeVblf@0{W_IxhCkdnh2|!P<-5l1TALy'
    'RP6W(<h8ld-|q5;&8PMSs|-1Kf>TxGPbi}>O0R%IYnF#+?QXAp+A_UlRXTGW4xLASr&&Q+6`}5g;jw7VDfjHBdppg>z_`vu0y^CS'
    'QZN$AVq)ECD3J%=@R}}pkMh7u=MrOsYkOoaOF~sSoy}2q{4im!uQ}6D4jizM+Eb+b3yn;eP&A*EcP#&7T>%94Xk~HPGG}q912TPy'
    'P~^*OuE=L&CD*O2R~3K@(sKS~d{}2b8Eye0BR-hG%0yW-d&E?AQ8k*A^bb8z(&o0Y8YZM_<1M@NnKwajxEFgDfN5PQQW%Fz6_OBn'
    'FfK7oJaawQvH{B%7JBFOvfz`MR>W^u{jaWhSeW>G&w>r+G8=vWZ-Gbz-_gRAZvtcHLhKn|^#>bif$E|KWvIs=-LUgdCBOt5&G3w5'
    'D?3;$8sIP9Jj!)Ou?|#kO8fLK+LVU8$y8NGPNBDID1_>NK_jO!0xfs*bM_xF0FBqBwq<;Soq4{qH>#>00~|ssv!xvha6GU5o{9oL'
    '6qtAaP{F1S@4lwC!pJ^i7dbJ6keFlY2^RJLKs}Fgk}iN~v(<>thckzq7Y}`RWFEg0be(0|jl_S(YxvNQ&3^y|zp3R5K8v3&D9^jo'
    '25WR1tXY@Nv_TwdZ-YKqQjl8UTH5{@u<ngJ9YD$ckGw@R_R0rp(#x;x*+9I1ZoBz@JyKAR-1>oa@NFo7f5uDkIl=az!NFoi`RfnX'
    'c)2@?L<=~oYy*}Rl)u51!a1c2AR|#ecC}@tz$3E2rfahVWa0%lR(qaMP7hRa@y3KVH)fz0!Xg;C=G@u!S{jJEF2rAqKAy8#kKhV!'
    'j|(ptnS=a8#eJUziZ=ne{q8|GOSo-jOu9|B?aM7()XIyKt-8H<N6%^5prN1Yvz!5mwm4BmEL#ae2YUqP;u<53y8;?CwuE$xb=^Dq'
    'QTAL!=LSfZ=~9YWF-SU@6@=bmt<u8-C>dC_FPU-?G{Aqw!VARz!>7h9<#y0Eg%}bS>s7j(31u#37Bf?7WuDu&Ey4S9m-<V<Pmx&e'
    'zQ+FwCAD^`|Iw$Ns+<fWAB`yl5qC}l2h~@sUJPdfdM<c&PcoW)I+&Kf&M9#7f=0l#$QXw^bhX@@uKLIu)4m*qvOFFP&)mm1(LJEo'
    'AsBta^^3#?6q1liu?bsx@frA>b*!rD^lphkuANo2suUi<*K}a_aAbrZo45Wq*LySwlbI=x2H}j4-o3DT99ojIhLi0i5=i%@4Sjis'
    'BMW^G2!$PGRx7xpIg)oXL^8)@Jke3@97kGmv9M?~5)ignS@{f#!<!iXr;_jVILBoR$EnPFm2+5~iTCFd@Tpd39V{A?Z&+2?NkQd-'
    'aVptX+uy`D`NTTWBevgtEl$!Yef+{Q#eQ!rLu+}-V!Ii%=w#Y|H>t7UM}=R{-hUfZ6KCg0*Z&I!lNuhk==;oZO|zK1PeDLAbQeEf'
    'W{jTdWW$4rr96ESoc;GuZUbt<58Sp+gka)C`w=2a-!;<YS&^!+9w-q5BED;CXv1O8(WAi{;Qh$g57A(GbIJNu2Hc`E(6QG#;&B&n'
    '-9u6p8?rDh7Wj^@)lAX>vVOrK0z$VV`1*p1xy&SuD`1vLSA(x!M34sYA-)fkiT}%g^VV^*DCA*=%wCaHA9E}Thyk+>E=X*Jpq6E8'
    '<$6;?L0|Xt(UvM6cD(^YBGGClbdcbMrQy8tzU@!g*6$5)2209T-qI+BJF(+mmUwgZ$9nXpx9xw|5SmQZAyk>L&_(=u?%RTw{V+;7'
    ')+0D1*V`Ptz59cJK$_X5k9aH>11n_SEtM#Ni--!RNS0i*f%yhID!(!+HM1{xuSyB>@}Usb|L8Mc$dd^}q7Y=<T+qx*8_g0jBWs0P'
    '&%(g7=;|P(nq5k5SRqQkbZn)-fg_>(SCl`p%Y6PsWEKGEvKH$DUj)SijS}#C5(#qroxa$2`p`_P(rlFDj2VzGhaId?`TK2kIr03%'
    '77pg!Q+6CRSqR>t*enx-{Bj^5FOTr^`2v}cV4B>ww5djSHf{%kvj;C@+tera$Kv^g8=bvXPA`SfX|T%eQ1$MA?i6DvY!D!KAn-u_'
    'dw5U4wSqMq;Vhm+d|KjS|NOYiuN0~pEf&shE~wfQ^m{ow{ZnjDXUwYo<WVi=CH9y15|i0v*#D@emc^PQgOCD@0el@jm@ecugVeE?'
    '0xEWt*Q0L35VvbJQ>aDw0YB}4wwB!292oDlW@oP+B}k}2Voy&WMq6+)5A)*VcI)IvnP3*ErR1RZ&ed-}v0<$68Bie+$s<WW2atrs'
    'yUI`LH3_C5sU%S(NLq}vUQZ{tZfa_}{IJ-qC=hR0=}AgA0nsV;+Uh{Rr)+n;7ios7DaGu4#~4`cY59ERZ?7a=z=s%fz3=B^5r!a>'
    'qldROYVZ-p(U&BPA5ov&#~B~c|BdS@Vpz5wkLr7_KMtP#{LH=CG9Thm0`)|QX5Rtl1RN>~G(RmWKO4+w?#44joWzTDM^il?&jT{D'
    'VUSXiCtk3okW3J*pRz3L+KetH5<4?;mPaz%*{#RTnI`A(qpYB=T5?2qw^~7pSoJ1w3O9OEb<@3fuy*wxO1av48JmPNAIFp^l$~Q3'
    'Du~KC4L_$KB@O!~6T7gyep7AL7!qAGUm6Sa=HLa-Lb!#~{=p)XLEkxc05%rA`*Vt`AlpYWJ3<Y}tIPrzOM*@uB8kaHjK7>L?>5g='
    '>P0G~+VBxXx67QHz~Mum=yl=nxdI_eT%;|K#=>fXFn}fzq+aPH>}tx;sX8Xy>v)%)VJ>P$5#^<jJy9}mCa?e~g2pH(3it%Z&(~Ur'
    '^k66wnu{~_EQVWB#F_vsQP*&2%}BJuTiIlOoBu$qc}&>rOiw!B@0IvLo@MixgV%z$<fdn^cY#}VS}sius<EVt&GL)mfQNpZpoYit'
    '+m=rq$>B6N`2BFQJw)fj$Dn`g<tY~(F|q<$2IuKxItR&kLH@9z7|FuiKR_^<^F?=*jI#;_9)V*?6vCM)vx|VqJBq8v3YUP{;KE(;'
    'yIHyT1@}DuRmHvqb>qhCC?M%4!~`KN3hu6zk~c}LiHX5}uJoQ?xyOfrRvJHp;PZ*4y1-4U?4#iYnjXN8c*U?uy>OD3A#-hPyJ<;V'
    '8iNxrG#r0doSjJMCsIC%FDg48eDU0!SPCxho8?~3ODB5AA;5&7BoKHMk2$*|pE~>#PHmM9sWBj)`A7{0;P-wIdsgUoACOR+m_AyY'
    ')t;0ae#$TPGEZhqs3!3uXI~!9tqrcK__O5_%_Fy*(iuyRg2-YjEV6R+DMj~HvpbY^r^S9C1UFgvfZ0I~v9*D%dgI$dF3?y_XnSTe'
    'LuA^W1K}clYIIOw0lXPXq2u@p+=X~mNX`$q%05pO*n{DtS-VgW`_j~%BJwS+-3CAaMg+f0Q^6}KWLmFN3=uQ>Vc`$V9@16NGxTdW'
    'mCHwDsU4XT*&UI@2f+K6J5_dFL+_elZ3Go#RqAY)aodvc;*im4MTH=+BREIkjO*A3LZCQPuW1A8bgkopDZHMgkwvbMWSqY&q$}Qw'
    'acf~zm)$g{-ffq=Ojue_f1R59c0AenBhELC>s4wfA}$XBFh8tNTaA90&#o9wWJf>gn?4em1Kz`NI{I@M{>;0VD;4Y85s6&N`%D~}'
    '<~LiKIQ+yiYxO?zWj-#@nzB4LYIB%TsEJ|1y#CCVezs-dr;pzo8ko$&0H_{ZAx?U%?~~Yt^X+miZ}}9+Jni>68DK-1use}$l<E<+'
    '4%gS0fc=ubMZP=FGY-UwuGh9)PS4IU6<;)?26pv>TL**Nv1}<E?&y}<${SIiIQvcT%<%BD$|7{ZOLr*dZDb;5NOtmnrIxY`R8q){'
    'VX7?@jX)_14+7nUT134-!1t_qeW#w8PyoYu2tR%Cs`(c5eLif!N(PxLapeMVTESa*^KflGq?o;|k6I6E_^<-|DS{@(u9OzQm0Kz0'
    'Tjv-f>kbSy8EbB|9Qb&dBW7x*tX*(>=P_%5fr(Hi`Tu6YUsVK=K=??HtBck8Qie^Pyg|&?Btl=xO4#Kt-S^@&EEAV0l|L$Z-1pnx'
    'z^!5IU(DQ{Se#e6&}%pRlrt5MV3iJEW9~3~fvizOXOVZevx;@6YJ|PVL%6`NChUt2D?gJ!U_v27SeIBg<jR{3#=Z!Gg%2VTS!YQN'
    '>Vxd%3TdmTGFz%^m^dKERx`E>bK;vs?*j(WzB4-v@t^OUDyb5D>K`>P>L^ImB3=s#erkHU$qIeQse8JRfHTne;^{%s9&{uw{!8Gs'
    'io~7qUha@o)d>yIDU<PbmxP`<X4dS6TtH(YZMMm8i+QN@OH8x)OdZWIg%0%?5qs{8h}yvJiXPiBc(a@_*-lZ##5KHoPRgtlIh6wX'
    't`6xSc^>t<D{G_AsSl{4qQ_1UQAinUxXF<GB#~!oiD{E>RP30hX7D2#E|a)S-B@qo5aH%idF}TSPz%*=?{A-5%ZrK_KV!50Dt%Vh'
    'd+@M!<t~08u*G;J3jyI%|5wH`wnfy<oF3eSE&wYn#;D1c3*fR*3%^vi*M8+O*NxY3u12^+!k^DPQb_(P_M)d?N&P^iQIFlk`)Kzf'
    '5pAYJwQIM*sNNs3S;PY*)r|IC{|0X)+Y0f-u~?Fa1j>d*eienqmY?!VKQe}tt)I55OZB9x*0-YEMxvw|$PT-#6vJ?)o61~?-A$-T'
    ')MjJRAQRGfJe%u%%Q){}lfM|z%m6YAgng~w%jHlYk-zjf`m%P4dxzdUNqP$ZukR?VDrJ^~Kc{~dZwhD~{CD_%zYe^|hNcF#wj9S6'
    'YS(H~JK!b?&*|5GqZ3=1>Idro)(D|&v;~%eD30CKa3@r`?FyX7(HqPyEyS=H6*(8!$VJ<#g}XVEcdlzONlSwUEvCXarA!3yDjcoh'
    '`}uP<vDu_!iPOlq<&zln0eYWrFHec>zWd$<_O2FSH|C8$&!as`Ot~@zEsm3G!K3ics?tNfC3X<lncGeBK<BHs5qxGm)HcA|@cYNh'
    'enAh@J!kArs!INTN4v&x4(+9j>#JR=3EEx{tWxO?Y$_$KY@PvrH>w-~7;<qY*gONF#Qfh90v_)nMASX3=1ev`ceTpSfeKU=&}^GZ'
    'i3I;J0=K8&bFFF;8MaCC<UWVX0JN9?7gh_JO{U@QVItINb6;n;U|Wnb>b(k~OZL!BgB7bv!A;U7*ZcmHW)Anp#cuoks_a&YOLV=N'
    'RAGk^H(NR715I~5XC~?X3oJa#jHNA2oUgt?s9rcZ(=ZeUIYY<=j2uu;)T7!7y)iugqZFjviB#BUr6RtH@(#NJCBTwDCvLo>P>9v#'
    'Uh)jN5SPrFsyy>6+8wYO+*mV26`yLrcORmPpk*Av3F_>f!Enx5Hq6}OvBJ*Gzf_3@xVW8!`mA3W{^l4$xGfsNLlB?VHwYBWx^k%z'
    '1!B-aXZwLbK#Vk~Bscz4vwH-Y<8clA^Z#{c!qzpPk5TPTcu!m;+-T5?&t*Z+)DKCorCu;Z3>BDyvz+=&&}=7x&+W?kpF7A@9i8y3'
    'm_cvV*fqIuFqt9jK7hls<Zk&hxU%13wDwKCd~2bWxtnLY9kjw%*1CIv2^Ox!kQ{3t3z6-ka`tTYC_OtQkQna&-`0O4SvtoU$Q1{i'
    'WUNg=9me!`*@fhoxXBE7wUWbY<m~#MXA$YPSA979w*Pl!f2<Y*{^5_iT*4f`W}hN&&W0OCfLSNKIwW*cUzf&o1Oet>L=_zcvC;Rn'
    '-SU=(jy)O)QPUh$Y?YqD=0!r>@@qPat(ixuf~J=~a7D^fg9moXDT_LmP6XkS+unww)Qv%Jf)n;IxUG25YU0`uDCRS-R02i@%dE(Z'
    'J&VlpBOIy_YvyHT+gVx?{E&2F4AcABQU=Q?|C1U#npy0{&aIP3OWU7jDt+~V(<*k_*^!fQi5c#eQT1Lu=2<*shf-O^hIlj340H1F'
    '$0`&5;h$zAjtv-6yxa;3^1CLHoZ^Qz5juw#r~q!QJfh<S9^p;Vf)@+L9z?qEErw2)^XzzxJ4WAco+6f&D%k)}ID}rsQEjdm4Xrlr'
    'Wsa}16F4iQp7abeZW&C@!c~litDOA$81v|tU9|xT)x7M4h+d^&;O{anHbLP5y?hka)zn##cmLZFVl>2ck{G<fAw9HT?It)p#9*e*'
    'c4vf@787vVgGW>TI`-1|43se1-IB`;nw^gquM~{|(et{i=^pZ_^H&c`PlxbWV>eh$MnZ~0e3Pc7fj@<a7Q%H?H7UxuP;l|H>fPa&'
    '^|{5IAE>jv_2iw<lKwoW#k8L6Lo$C1=N;HdJ;BLk%41DZ>)oH+l8oKKCkw*e;SkQiV)wOGrp>9(bl<F5>M3_R7lK6oeGXl!2a<vr'
    'LX9Kin3imp<j#_H72;w>e&C~B*eGbOT|_N#4AVwnj>dHt&+pDVEdf(-9$HumwydkPz{nepWg)S^Xq{9vJ*Xyecl7`cu8Pj6ufYIC'
    'VotZ(UmSDf0{GELa}BDRZ>YK{Gh9{ORzG-baEbjrS}b)0#*oxrSw}}}<M=nhIKP)I27~4T$Ctj^p(9yS;&`S=*o=Y$9q{k0SL-gu'
    'se=m4({!PBat-h8cLQoOMy+#cTOZMRWNWjqZh(Q>CbT%eIs!-Pql<355ZYgwh5b7i2l#Om9=H;9`Q<_bj@qB*^Qhcac8L^BbWmF('
    'H9$f<gY!69K#APi8uHL0J=Wg;k=Ss#*{cXuHf3&;!Plka>kgtAz`GNY)MsJ;UHAN>#wM6oR~h+P+#KUCyf^VlwgGxTTfwml6nC<p'
    '1U}5XDYL2JPZN9oBMjt!$$#j)e4^5?Dp49{;iN+UuEf76!mSLP@zZ7i&C{)!SId}a^6HS~2RX~W>`0S$e!VCaJZzSfyvePQczKwR'
    'c2mI@><^2FG=>EJswn`c%gz)B#ez?M%lJOwCeIelYS5{pj|o9onE(*j-6v`-QHNSqQAEZ9as@aJOc!qZ^jn!kkSnL&$HcA?gR0%K'
    'veo=FjLF<-bz+npffPT1?JNys?vHrx_w^~YzqSl#-6?^==chWhihG`5$AQcX5XElcGi%p;CxsDd{wK>h>tu^Vc%@Eg)npBL1TqK_'
    'DhZUniqSRWtYt|QI&_(VE_otF6#o2yJPs)#-U-NpRqVr>{GYpT>KB!RQ3_EiPJ^nR_Ajmug8c*(B6|M7-QPz3i8<&BDB2B(w+L{s'
    'w*sgh9ITlv+%;c?u{4v!o?RS=Y{>>QlBN+$Z;y5}d|ONplg*wg3*UY0fhghIk9@O+cO2Xld0<+-mi#ukrmwaZe``2dlOV3TN{G^*'
    'KZtkfd-KPmZ&LnX?WS<vPH>9jE`F(n^%+6~?NCE%bIo}cK91+(1ol&h<e`-lRM}aJ4RyTU1!Rpc^2rBtdSFC!$=-%o*gN3rYkAmq'
    '9SkX+RSL&T3VK@Lnw)32Oi-S}{N}~Xhav|0nD2Z5DHkhVa}BwE00Eqv0rvkK-re_svBYQl0ssI200dcD'
)))
parser = argparse.ArgumentParser()
parser.add_argument('--runner', required=True)
args = parser.parse_args()
ok = normalize(Path(args.runner).read_text()) in ACCEPT_BODIES
print('TALLY_AUDIT: ' + ('PASS' if ok else 'FAIL'))
raise SystemExit(0 if ok else 1)
```

The allowlist embeds all six full normalized bodies returned by v1 `frozen_accept` at build time, not hashes and not runtime lane reads. They have 4 distinct normalized bodies. The source payload is an LZMA-compressed, base85-encoded JSON array. Build input is the pinned runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. Normalization removes every whole comment line (including `# nonce` and decoys) and sorts the tally loop's operands. Inline comments remain part of the body. The sandbox exposes only the tool and one copy, not the lane or counter. Held-out acceptance is exactly **0/12**.

### Control (d) — Runner selftest passthrough

- Source: `/fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/controls/d.py` (full exact source below).
- Tool SHA256: `66df356629807adb890d09e0f27cb4055869bbbb7ba2902347d8f803757572d5`.
- Sandbox commit: `602131c59c8aaf0352c6cb1c97cfaf9fa5dc7d2c`.
- Counter copy SHA256: `44dafb3cc2286632bcba39dade0edc02b0a1fd583ee12248e586ffc99c0b9224`.
- Expected detector: `C1_R32V2_PASS=false` (counter exit 1).
- Observed exit: `1`; elapsed: `85.073` seconds.

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-d.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-d --seed 1
```

```text
C1_R32V2: v1_kill=2/18 v1_accept=8/8 ho_kill=1/10 ho_accept=11/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=602131c59c8aaf0352c6cb1c97cfaf9fa5dc7d2c C1_R32V2_PASS=false
```

```python
#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--runner', required=True)
args = parser.parse_args()
result = subprocess.run(['bash', args.runner, '--selftest'])
ok = result.returncode == 0
print('TALLY_AUDIT: ' + ('PASS' if ok else 'FAIL'), flush=True)
raise SystemExit(0 if ok else 1)
```

### Restoration evidence

A `finally` block checks out the original measurement revision and restores the exact original tool bytes and mode even if a detector raises. Final restoration receipt:

```json
{
  "head": "24a5a5bb598ae919546715267d76f814efaf8912",
  "tool_before_sha256": "9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef",
  "tool_after_sha256": "9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef",
  "runner_before_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
  "runner_after_sha256": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
  "exact_bytes": true,
  "mode_before": 493,
  "mode_after": 493
}
```

The runner's before/after SHA256 is identical. The tool's before/after SHA256 is identical and the byte comparison is true. Scratch HEAD is restored to the measurement revision.

Restored detector command:

```sh
timeout 180s python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/x/.ufo/evidence/round-32/v2/c1-measure-v2-pristine.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/clone --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlV2Controls/work-restored --seed 1
```

Observed exit: `1`; elapsed: `33.329` seconds.

```text
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

## Smallest correction

No production code change. Label these as post-data control receipts; the missed before-data control check cannot be repaired retrospectively. Keep the original first-v2 miss unchanged.
