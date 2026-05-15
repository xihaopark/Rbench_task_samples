# Case 40 - `chipseeker/H001_annotate_peaks`
**Track:** `omics_core`  **Package:** `chipseeker`  **Function:** `annotatePeak`  **Level:** `L2`  **Agent sample:** Biomni `sample_00`  **Evaluation status:** `FAIL`
**Evaluation message:** Failed at case_01_seed_1000
**Sample status counts:** `{"FAIL": 5}`

## Task Prompt

```text
Write R code to annotate ChIP-seq peaks with nearby genes using ChIPseeker. At the beginning, load the required packages: library(ChIPseeker). The goal is to interpret which genomic features your binding sites fall into (for example, promoters, exons, or intergenic regions) and which genes they are likely to regulate, using the BED file at inputs/peaks.bed as input. Use readPeakFile() to load the peaks and then annotatePeak() with tssRegion=c(-3000,3000), TxDb=TxDb.Hsapiens.UCSC.hg19.knownGene, and annoDb="org.Hs.eg.db", relying only on ChIPseeker and its documented helper annotation packages rather than bringing in any additional toolkits; be sure to carry through the full annotation object without dropping fields so it can be used downstream. Save the complete csAnno object as an RDS file to outputs/annotated_peaks.rds and also export a tabular version of the annotations to outputs/peak_annotation.csv, and as a quick quality check confirm that both files are created, look at the distribution of annotation categories around TSS, and check for NA-heavy columns or obviously malformed entries in the output table.
```

## Input Files

**`inputs/peaks.bed`**

```text
chr3	198108	198434	peak	151	+
chr5	147186	147292	peak	673	+
chr4	28736	28923	peak	263	+
chr5	197693	198012	peak	382	+
chr3	68589	68842	peak	21	+
chr2	178555	178707	peak	379	+
chr2	186955	187375	peak	342	+
chr3	104408	104796	peak	882	+
chr3	73455	73918	peak	193	+
chr2	42433	42718	peak	676	+
chr1	64425	64659	peak	50	+
chr3	60489	60831	peak	156	+
chr2	31625	31786	peak	729	+
chr2	167269	167388	peak	594	+
chr4	9164	9526	peak	792	+
chr1	37716	37985	peak	563	+
chr3	87681	87881	peak	851	+
chr1	37566	37954	peak	562	+
chr5	52067	52521	peak	403	+
chr5	47770	47985	peak	803	+
chr5	119530	119698	peak	672	+
chr4	131979	132105	peak	204	+
chr2	95179	95442	peak	761	+
chr4	103829	104031	peak	968	+
chr1	16720	17008	peak	916	+
chr4	164947	165280	peak	78	+
chr5	28843	28996	peak	363	+
chr1	38741	39054	peak	667	+
chr4	93783	94102	peak	127	+
chr1	196115	196528	peak	381	+
chr2	68925	69106	peak	569	+
chr3	79176	79367	peak	417	+
chr2	55697	56108	peak	89	+
chr5	91237	91494	peak	678	+
chr4	171138	171456	peak	108	+
chr5	55582	55809	peak	871	+
chr4	140792	141146	peak	815	+
chr2	65230	65663	peak	713	+
chr5	67300	67427	peak	692	+
chr3	125855	126284	peak	224	+
chr5	8868	9350	peak	557	+
chr5	86841	87287	peak	275	+
chr1	86894	87073	peak	620	+
chr4	16243	16456	peak	358	+
chr4	142469	142682	peak	520	+
chr5	20624	20981	peak	867	+
chr3	149181	149426	peak	332	+
chr2	14229	14335	peak	505	+
chr1	115120	115397	peak	602	+
chr5	141842	142097	peak	710	+
chr2	137193	137461	peak	628	+
chr5	181789	181895	peak	314	+
chr2	87145	87264	peak	770	+
chr4	81105	81356	peak	151	+
chr2	115157	115431	peak	727	+
chr1	101109	101294	peak	296	+
chr5	51137	51305	peak	355	+
chr1	49135	49470	peak	198	+
chr4	68970	69214	peak	521	+
chr1	140049	140515	peak	906	+
chr1	199128	199499	peak	801	+
chr2	177253	177746	peak	567	+
chr2	38473	38846	peak	907	+
chr4	187149	187410	peak	615	+
chr5	98999	99130	peak	730	+
chr5	39440	39884	peak	548	+
chr1	92425	92559	peak	317	+
chr5	191860	191994	peak	366	+
chr1	65447	65771	peak	510	+
chr1	135323	135583	peak	921	+
chr2	174665	174813	peak	780	+
chr3	148399	148825	peak	416	+
chr3	40266	40674	peak	829	+
chr4	87378	87633	peak	737	+
chr5	92244	92545	peak	560	+
chr3	124379	124603	peak	677	+
chr1	127987	128323	peak	161	+
chr1	106400	106756	peak	107	+
chr3	33346	33717	peak	106	+
chr3	132314	132464	peak	221	+
chr3	83016	83381	peak	977	+
chr4	159796	160287	peak	663	+
chr1	135746	136146	peak	404	+
chr2	27319	27473	peak	463	+
chr2	67801	68134	peak	736	+
chr1	173391	173695	peak	189	+
chr1	185299	185586	peak	788	+
chr4	141742	142067	peak	916	+
chr3	20076	20424	peak	539	+
chr4	70166	70588	peak	161	+
chr5	152602	152936	peak	535	+
chr5	83575	83802	peak	219	+
chr4	7177	7328	peak	912	+
chr3	55840	56248	peak	473	+
chr5	29506	29931	peak	342	+
chr2	93227	93641	peak	735	+
chr3	181251	181715	peak	312	+
chr1	88649	89146	peak	20	+
chr2	139283	139536	peak	578	+
chr4	22480	22958	peak	231	+
chr4	9849	10161	peak	463	+
```

## Reference Code

```r
#!/usr/bin/env Rscript
library(ChIPseeker)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)

peaks = readPeakFile('inputs/peaks.bed')
peakAnno = annotatePeak(peaks, tssRegion=c(-3000, 3000),
                        TxDb=TxDb.Hsapiens.UCSC.hg19.knownGene,
                        annoDb="org.Hs.eg.db")
saveRDS(peakAnno, 'outputs/annotated_peaks.rds')
write.csv(as.data.frame(peakAnno), 'outputs/peak_annotation.csv', row.names=FALSE, quote=FALSE)
```

## Reference Output

**`outputs/annotated_peaks.rds`**

```text
[binary file]
size_bytes: 5175
sha256: 339e9e4c4b12fd82bf97e900133ae1ce5b7e032a375ae1a882e99d7b50963830
```

**`outputs/peak_annotation.csv`**

```csv
seqnames,start,end,width,strand,V4,V5,V6,annotation,geneChr,geneStart,geneEnd,geneLength,geneStrand,geneId,transcriptId,distanceToTSS,ENSEMBL,SYMBOL,GENENAME
chr3,198109,198434,326,*,peak,151,+,Intron (ENST00000663345.2_6/101927174, intron 1 of 2),3,237440,238224,785,2,101927174,ENST00000757007.1_1,39790,NA,CHL1-AS2,CHL1 antisense RNA 2
chr5,147187,147292,106,*,peak,673,+,Intron (ENST00000637938.2_8/153478, intron 6 of 19),5,140681,157225,16545,1,153478,ENST00000502646.1_3,6506,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr4,28737,28923,187,*,peak,263,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-24257,ENSG00000272602,ZNF595,zinc finger protein 595
chr5,197694,198012,319,*,peak,382,+,3' UTR,5,191610,196449,4840,1,389257,ENST00000328278.4_4,6084,ENSG00000185028,LRRC14B,leucine rich repeat containing 14B
chr3,68590,68842,253,*,peak,21,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,3159,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr2,178556,178707,152,*,peak,379,+,Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4),2,222361,231159,8799,2,26751,ENST00000472012.1_3,52452,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr2,186956,187375,420,*,peak,342,+,Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4),2,222361,231159,8799,2,26751,ENST00000472012.1_3,43784,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr3,104409,104796,388,*,peak,882,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,38978,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr3,73456,73918,463,*,peak,193,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,8025,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr2,42434,42718,285,*,peak,676,+,Promoter (<=1kb),2,41220,42952,1733,2,642273,ENST00000460464.1_3,234,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr1,64426,64659,234,*,peak,50,+,Promoter (<=1kb),1,65419,71585,6167,1,79501,ENST00000641515.2_6,-760,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr3,60490,60831,342,*,peak,156,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,-4600,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr2,31626,31786,161,*,peak,729,+,Distal Intergenic,2,41220,42952,1733,2,642273,ENST00000460464.1_3,11166,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr2,167270,167388,119,*,peak,594,+,Intron (ENST00000775033.1_2/ENST00000775033.1_2, intron 3 of 3),2,222361,231159,8799,2,26751,ENST00000472012.1_3,63771,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr4,9165,9526,362,*,peak,792,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-43654,ENSG00000272602,ZNF595,zinc finger protein 595
chr1,37717,37985,269,*,peak,563,+,Promoter (<=1kb),1,34553,37595,3043,2,645520,ENST00000834250.1_2,-122,ENSG00000237613,FAM138A,family with sequence similarity 138 member A
chr3,87682,87881,200,*,peak,851,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,22251,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr1,37567,37954,388,*,peak,562,+,Promoter (<=1kb),1,34553,37595,3043,2,645520,ENST00000834250.1_2,0,ENSG00000237613,FAM138A,family with sequence similarity 138 member A
chr5,52068,52521,454,*,peak,403,+,Exon (ENST00000846714.1_2/ENST00000846714.1_2, exon 2 of 2),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-39762,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr5,47771,47985,215,*,peak,803,+,Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 1 of 4),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-44298,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr5,119531,119698,168,*,peak,672,+,Intron (ENST00000637938.2_8/153478, intron 2 of 19),5,140373,190087,49715,1,153478,ENST00000283426.11_5,-20675,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr4,131980,132105,126,*,peak,204,+,Intron (ENST00000510175.6_4/255403, intron 1 of 1),4,124420,156491,32072,1,255403,ENST00000609714.1_2,7560,ENSG00000250312,ZNF718,zinc finger protein 718
chr2,95180,95442,263,*,peak,761,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-48310,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr4,103830,104031,202,*,peak,968,+,Distal Intergenic,4,85621,87340,1720,1,152687,ENST00000380882.5,18209,ENSG00000272602,ZNF595,zinc finger protein 595
chr1,16721,17008,288,*,peak,916,+,Promoter (1-2kb),1,14409,18061,3653,2,653635,ENST00000831739.1_1,1053,ENSG00000310526,WASH7P,WASP family homolog 7, pseudogene
chr4,164948,165280,333,*,peak,78,+,Intron (ENST00000642529.1_1/255403, intron 1 of 2),4,124420,156491,32072,1,255403,ENST00000609714.1_2,40528,ENSG00000250312,ZNF718,zinc finger protein 718
chr5,28844,28996,153,*,peak,363,+,Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 2 of 4),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-63287,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr1,38742,39054,313,*,peak,667,+,Promoter (1-2kb),1,34553,37595,3043,2,645520,ENST00000834250.1_2,-1147,ENSG00000237613,FAM138A,family with sequence similarity 138 member A
chr4,93784,94102,319,*,peak,127,+,Distal Intergenic,4,85621,87340,1720,1,152687,ENST00000380882.5,8163,ENSG00000272602,ZNF595,zinc finger protein 595
chr1,196116,196528,413,*,peak,381,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,-55777,NA,LOC729737,uncharacterized LOC729737
chr2,68926,69106,181,*,peak,569,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-22056,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr3,79177,79367,191,*,peak,417,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,13746,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr2,55698,56108,411,*,peak,89,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-8828,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr5,91238,91494,257,*,peak,678,+,Promoter (<=1kb),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-789,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr4,171139,171456,318,*,peak,108,+,Intron (ENST00000642529.1_1/255403, intron 1 of 2),4,206367,249774,43408,1,642280,ENST00000356347.4_4,-34911,ENSG00000290382,ZNF876P,zinc finger protein 876, pseudogene
chr5,55583,55809,227,*,peak,871,+,Intron (ENST00000846515.1_2/ENST00000846515.1_2, intron 1 of 1),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-36474,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr4,140793,141146,354,*,peak,815,+,Intron (ENST00000510175.6_4/255403, intron 1 of 1),4,124420,156491,32072,1,255403,ENST00000609714.1_2,16373,ENSG00000250312,ZNF718,zinc finger protein 718
chr2,65231,65663,433,*,peak,713,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-18361,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr5,67301,67427,127,*,peak,692,+,Intron (ENST00000846515.1_2/ENST00000846515.1_2, intron 1 of 1),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-24856,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr3,125856,126284,429,*,peak,224,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,60425,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr5,8869,9350,482,*,peak,557,+,Distal Intergenic,5,92283,190081,97799,1,153478,ENST00000637938.2_8,-82933,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr5,86842,87287,446,*,peak,275,+,Distal Intergenic,5,92283,190081,97799,1,153478,ENST00000637938.2_8,-4996,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr1,86895,87073,179,*,peak,620,+,Distal Intergenic,1,65419,71585,6167,1,79501,ENST00000641515.2_6,21476,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr4,16244,16456,213,*,peak,358,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-36724,ENSG00000272602,ZNF595,zinc finger protein 595
chr4,142470,142682,213,*,peak,520,+,Intron (ENST00000510175.6_4/255403, intron 1 of 1),4,124420,156491,32072,1,255403,ENST00000609714.1_2,18050,ENSG00000250312,ZNF718,zinc finger protein 718
chr5,20625,20981,357,*,peak,867,+,Distal Intergenic,5,92283,190081,97799,1,153478,ENST00000637938.2_8,-71302,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr3,149182,149426,245,*,peak,332,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,83751,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr2,14230,14335,106,*,peak,505,+,Distal Intergenic,2,41220,42952,1733,2,642273,ENST00000460464.1_3,28617,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr1,115121,115397,277,*,peak,602,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,24942,NA,LOC729737,uncharacterized LOC729737
chr5,141843,142097,255,*,peak,710,+,Promoter (1-2kb),5,140681,157225,16545,1,153478,ENST00000502646.1_3,1162,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr2,137194,137461,268,*,peak,628,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-90324,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr5,181790,181895,106,*,peak,314,+,Exon (ENST00000637938.2_8/153478, exon 19 of 20),5,191610,196449,4840,1,389257,ENST00000328278.4_4,-9715,ENSG00000185028,LRRC14B,leucine rich repeat containing 14B
chr2,87146,87264,119,*,peak,770,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-40276,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr4,81106,81356,251,*,peak,151,+,Intron (ENST00000608255.2_3/152687, intron 1 of 2),4,85621,87340,1720,1,152687,ENST00000380882.5,-4265,ENSG00000272602,ZNF595,zinc finger protein 595
chr2,115158,115431,274,*,peak,727,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-68288,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr1,101110,101294,185,*,peak,296,+,Intron (ENST00000833190.1_2/ENST00000833190.1_2, intron 1 of 1),1,65419,71585,6167,1,79501,ENST00000641515.2_6,35691,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr5,51138,51305,168,*,peak,355,+,Exon (ENST00000846714.1_2/ENST00000846714.1_2, exon 1 of 2),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-40978,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr1,49136,49470,335,*,peak,198,+,Distal Intergenic,1,34553,37595,3043,2,645520,ENST00000834250.1_2,-11541,ENSG00000237613,FAM138A,family with sequence similarity 138 member A
chr4,68971,69214,244,*,peak,521,+,Intron (ENST00000608255.2_3/152687, intron 1 of 2),4,53223,60407,7185,1,152687,ENST00000502981.2_1,15748,ENSG00000272602,ZNF595,zinc finger protein 595
chr1,140050,140515,466,*,peak,906,+,Promoter (<=1kb),1,139790,140339,550,2,729737,ENST00000493797.1_5,0,NA,LOC729737,uncharacterized LOC729737
chr1,199129,199499,371,*,peak,801,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,-58790,NA,LOC729737,uncharacterized LOC729737
chr2,177254,177746,493,*,peak,567,+,Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4),2,222361,231159,8799,2,26751,ENST00000472012.1_3,53413,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr2,38474,38846,373,*,peak,907,+,3' UTR,2,41220,42952,1733,2,642273,ENST00000460464.1_3,4106,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr4,187150,187410,261,*,peak,615,+,Intron (ENST00000642529.1_1/255403, intron 1 of 2),4,206367,249774,43408,1,642280,ENST00000356347.4_4,-18957,ENSG00000290382,ZNF876P,zinc finger protein 876, pseudogene
chr5,99000,99130,131,*,peak,730,+,Intron (ENST00000637938.2_8/153478, intron 1 of 19),5,92283,190081,97799,1,153478,ENST00000637938.2_8,6717,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr5,39441,39884,444,*,peak,548,+,Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 1 of 4),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-52399,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr1,92426,92559,134,*,peak,317,+,Distal Intergenic,1,65419,71585,6167,1,79501,ENST00000641515.2_6,27007,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr5,191861,191994,134,*,peak,366,+,Promoter (<=1kb),5,191610,196449,4840,1,389257,ENST00000328278.4_4,251,ENSG00000185028,LRRC14B,leucine rich repeat containing 14B
chr1,65448,65771,324,*,peak,510,+,Promoter (<=1kb),1,65419,71585,6167,1,79501,ENST00000641515.2_6,29,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr1,135324,135583,260,*,peak,921,+,3' UTR,1,139790,140339,550,2,729737,ENST00000493797.1_5,4756,NA,LOC729737,uncharacterized LOC729737
chr2,174666,174813,148,*,peak,780,+,Intron (ENST00000774826.1_1/ENST00000774826.1_1, intron 1 of 3),2,222361,231159,8799,2,26751,ENST00000472012.1_3,56346,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr3,148400,148825,426,*,peak,416,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,82969,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr3,40267,40674,408,*,peak,829,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,-24757,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr4,87379,87633,255,*,peak,737,+,Promoter (1-2kb),4,85621,87340,1720,1,152687,ENST00000380882.5,1758,ENSG00000272602,ZNF595,zinc finger protein 595
chr5,92245,92545,301,*,peak,560,+,Promoter (<=1kb),5,92283,190081,97799,1,153478,ENST00000637938.2_8,0,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr3,124380,124603,224,*,peak,677,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,58949,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr1,127988,128323,336,*,peak,161,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,12016,NA,LOC729737,uncharacterized LOC729737
chr1,106401,106756,356,*,peak,107,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,33583,NA,LOC729737,uncharacterized LOC729737
chr3,33347,33717,371,*,peak,106,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,-31714,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr3,132315,132464,150,*,peak,221,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,66884,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr3,83017,83381,365,*,peak,977,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,17586,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr4,159797,160287,491,*,peak,663,+,Intron (ENST00000642529.1_1/255403, intron 1 of 2),4,124420,156491,32072,1,255403,ENST00000609714.1_2,35377,ENSG00000250312,ZNF718,zinc finger protein 718
chr1,135747,136146,400,*,peak,404,+,3' UTR,1,139790,140339,550,2,729737,ENST00000493797.1_5,4193,NA,LOC729737,uncharacterized LOC729737
chr2,27320,27473,154,*,peak,463,+,Distal Intergenic,2,41220,42952,1733,2,642273,ENST00000460464.1_3,15479,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr2,67802,68134,333,*,peak,736,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-20932,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr1,173392,173695,304,*,peak,189,+,Intron (ENST00000466557.2/ENST00000466557.2, intron 1 of 7),1,139790,140339,550,2,729737,ENST00000493797.1_5,-33053,NA,LOC729737,uncharacterized LOC729737
chr1,185300,185586,287,*,peak,788,+,Distal Intergenic,1,139790,140339,550,2,729737,ENST00000493797.1_5,-44961,NA,LOC729737,uncharacterized LOC729737
chr4,141743,142067,325,*,peak,916,+,Intron (ENST00000510175.6_4/255403, intron 1 of 1),4,124420,156491,32072,1,255403,ENST00000609714.1_2,17323,ENSG00000250312,ZNF718,zinc finger protein 718
chr3,20077,20424,348,*,peak,539,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,-45007,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr4,70167,70588,422,*,peak,161,+,Intron (ENST00000608255.2_3/152687, intron 1 of 2),4,85621,87340,1720,1,152687,ENST00000380882.5,-15033,ENSG00000272602,ZNF595,zinc finger protein 595
chr5,152603,152936,334,*,peak,535,+,Intron (ENST00000637938.2_8/153478, intron 7 of 19),5,140681,157225,16545,1,153478,ENST00000502646.1_3,11922,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr5,83576,83802,227,*,peak,219,+,Distal Intergenic,5,92283,190081,97799,1,153478,ENST00000637938.2_8,-8481,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr4,7178,7328,151,*,peak,912,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-45852,ENSG00000272602,ZNF595,zinc finger protein 595
chr3,55841,56248,408,*,peak,473,+,Distal Intergenic,3,65431,66175,745,1,102723448,ENST00000440867.1,-9183,ENSG00000223587,LINC01986,long intergenic non-protein coding RNA 1986
chr5,29507,29931,425,*,peak,342,+,Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 2 of 4),5,92283,190081,97799,1,153478,ENST00000637938.2_8,-62352,ENSG00000153404,PLEKHG4B,pleckstrin homology and RhoGEF domain containing G4B
chr2,93228,93641,414,*,peak,735,+,Distal Intergenic,2,41221,46870,5650,2,642273,ENST00000461026.1_3,-46358,ENSG00000184731,FAM110C,family with sequence similarity 110 member C
chr3,181252,181715,464,*,peak,312,+,Intron (ENST00000663345.2_6/101927174, intron 1 of 2),3,237440,238224,785,2,101927174,ENST00000757007.1_1,56509,NA,CHL1-AS2,CHL1 antisense RNA 2
chr1,88650,89146,497,*,peak,20,+,Distal Intergenic,1,65419,71585,6167,1,79501,ENST00000641515.2_6,23231,ENSG00000186092,OR4F5,olfactory receptor family 4 subfamily F member 5
chr2,139284,139536,253,*,peak,578,+,Distal Intergenic,2,222361,231159,8799,2,26751,ENST00000472012.1_3,91623,ENSG00000035115,SH3YL1,SH3 and SYLF domain containing 1
chr4,22481,22958,478,*,peak,231,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-30222,ENSG00000272602,ZNF595,zinc finger protein 595
chr4,9850,10161,312,*,peak,463,+,Distal Intergenic,4,53180,87412,34233,1,152687,ENST00000608255.2_3,-43019,ENSG00000272602,ZNF595,zinc finger protein 595
```

## Biomni Code

```r
#!R
#!/usr/bin/env Rscript
# Complete R script for annotating ChIP-seq peaks with ChIPseeker
# Author: Bioinformatics Assistant
# Description: Annotates ChIP-seq peaks with nearby genes using ChIPseeker

cat("=============================================\n")
cat("ChIP-seq Peak Annotation with ChIPseeker\n")
cat("=============================================\n\n")

# Set up output directory
cat("1. Setting up output directory...\n")
dir.create("outputs", showWarnings = FALSE)
if (!dir.exists("outputs")) {
  stop("Failed to create outputs directory. Check permissions.\n")
}
cat("   Output directory 'outputs' created/verified.\n\n")

# Load required packages
cat("2. Loading required packages...\n")
required_packages <- c("ChIPseeker", "TxDb.Hsapiens.UCSC.hg19.knownGene", "org.Hs.eg.db")

for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    stop(paste("Required package", pkg, "is not available. Please install it.\n"))
  }
  cat(paste("   Loaded package:", pkg, "\n"))
}
cat("\n")

# Check input file
cat("3. Checking input file...\n")
input_file <- "inputs/peaks.bed"
if (!file.exists(input_file)) {
  stop(paste("Input file not found:", input_file, "\nPlease ensure the file exists in the inputs/ directory.\n"))
}
cat(paste("   Input file found:", input_file, "\n"))

# Get file info
file_info <- file.info(input_file)
cat(paste("   File size:", round(file_info$size/1024, 2), "KB\n"))
cat(paste("   Last modified:", file_info$mtime, "\n\n"))

# Read peaks
cat("4. Reading peaks from BED file...\n")
peaks <- readPeakFile(input_file)
cat(paste("   Number of peaks loaded:", length(peaks), "\n"))
cat(paste("   Genomic ranges loaded successfully.\n\n"))

# Annotate peaks
cat("5. Annotating peaks with genomic features...\n")
cat("   Using parameters:\n")
cat("   - tssRegion: c(-3000, 3000)\n")
cat("   - TxDb: TxDb.Hsapiens.UCSC.hg19.knownGene\n")
cat("   - annoDb: org.Hs.eg.db\n\n")

annotated_peaks <- annotatePeak(
  peaks,
  tssRegion = c(-3000, 3000),
  TxDb = TxDb.Hsapiens.UCSC.hg19.knownGene,
  annoDb = "org.Hs.eg.db"
)

cat("   Peak annotation completed successfully.\n")
cat(paste("   Class of annotation object:", class(annotated_peaks), "\n"))
cat(paste("   Annotation type:", annotated_peaks@annoStat$Feature[1], "...\n\n"))

# Save the complete csAnno object as RDS
cat("6. Saving complete annotation object...\n")
rds_file <- "outputs/annotated_peaks.rds"
saveRDS(annotated_peaks, file = rds_file)
cat(paste("   Saved to:", rds_file, "\n\n"))

# Export tabular version
cat("7. Exporting tabular annotations...\n")
csv_file <- "outputs/peak_annotation.csv"

# Extract annotation data
annotation_df <- as.data.frame(annotated_peaks)

# Check for NA values
na_counts <- colSums(is.na(annotation_df))
high_na_cols <- names(na_counts[na_counts > 0])

if (length(high_na_cols) > 0) {
  cat("   Columns with NA values:\n")
  for (col in high_na_cols) {
    cat(paste("   -", col, ":", na_counts[col], "NAs (", 
              round(na_counts[col]/nrow(annotation_df)*100, 1), "%)\n"))
  }
} else {
  cat("   No NA values found in any columns.\n")
}

# Write to CSV
write.csv(annotation_df, file = csv_file, row.names = FALSE)
cat(paste("   Tabular data saved to:", csv_file, "\n"))
cat(paste("   Table dimensions:", nrow(annotation_df), "rows ×", ncol(annotation_df), "columns\n\n"))

# Quality checks
cat("8. Performing quality checks...\n")

# Check if files were created
files_created <- c(rds_file, csv_file)
files_exist <- file.exists(files_created)

if (all(files_exist)) {
  cat("   ✓ Both output files created successfully.\n")
  for (file in files_created) {
    size <- file.info(file)$size
    cat(paste("     -", file, ":", round(size/1024, 2), "KB\n"))
  }
} else {
  missing_files <- files_created[!files_exist]
  cat(paste("   ✗ Some files not created:", paste(missing_files, collapse=", "), "\n"))
}

# Look at distribution of annotation categories
cat("\n9. Analyzing annotation distribution...\n")
if (!is.null(annotated_peaks@annoStat)) {
  anno_stats <- annotated_peaks@annoStat
  cat("   Annotation category distribution:\n")
  for (i in 1:nrow(anno_stats)) {
    cat(paste("   - ", anno_stats$Feature[i], ": ", 
              round(anno_stats$Frequency[i], 1), "%\n", sep=""))
  }
  
  # Check for TSS proximity
  tss_proximal <- sum(annotation_df$distanceToTSS >= -3000 & annotation_df$distanceToTSS <= 3000, na.rm = TRUE)
  tss_percent <- round(tss_proximal / nrow(annotation_df) * 100, 1)
  cat(paste("\n   Peaks within ±3kb of TSS:", tss_proximal, "(", tss_percent, "%)\n"))
} else {
  cat("   Warning: Annotation statistics not available in object.\n")
}

# Check for malformed entries
cat("\n10. Checking for malformed entries...\n")
malformed_checks <- list()

# Check for negative widths
malformed_checks$negative_width <- sum(width(peaks) <= 0)
if (malformed_checks$negative_width > 0) {
  cat(paste("   Warning:", malformed_checks$negative_width, "peaks have width <= 0\n"))
}

# Check for NA in critical columns
critical_cols <- c("seqnames", "start", "end", "annotation", "geneId")
for (col in critical_cols) {
  if (col %in% names(annotation_df)) {
    na_count <- sum(is.na(annotation_df[[col]]))
    if (na_count > 0) {
      cat(paste("   Warning:", na_count, "NAs in column", col, "\n"))
    }
  }
}

# Check gene symbols
if ("SYMBOL" %in% names(annotation_df)) {
  empty_symbols <- sum(annotation_df$SYMBOL == "" | is.na(annotation_df$SYMBOL))
  cat(paste("   Empty/missing gene symbols:", empty_symbols, "\n"))
}

cat("\n11. Summary of annotation results:\n")
cat(paste("   Total peaks processed:", length(peaks), "\n"))
cat(paste("   Unique genes annotated:", length(unique(annotation_df$geneId[!is.na(annotation_df$geneId)])), "\n"))

if ("annotation" %in% names(annotation_df)) {
  annotation_types <- table(annotation_df$annotation)
  cat("   Top annotation types:\n")
  top_types <- head(sort(annotation_types, decreasing = TRUE), 5)
  for (i in 1:length(top_types)) {
    cat(paste("   - ", names(top_types)[i], ": ", top_types[i], " (", 
              round(top_types[i]/nrow(annotation_df)*100, 1), "%)\n", sep=""))
  }
}

cat("\n=============================================\n")
cat("Annotation completed successfully!\n")
cat("Output files:\n")
cat("1. outputs/annotated_peaks.rds - Complete csAnno object\n")
cat("2. outputs/peak_annotation.csv - Tabular annotation data\n")
cat("=============================================\n")

# Return success
quit(status = 0)
```

## Biomni Execution Output

**`stdout.txt`**

```text
=============================================
ChIP-seq Peak Annotation with ChIPseeker
=============================================

1. Setting up output directory...
   Output directory 'outputs' created/verified.

2. Loading required packages...
   Loaded package: ChIPseeker 
   Loaded package: TxDb.Hsapiens.UCSC.hg19.knownGene 
   Loaded package: org.Hs.eg.db 

3. Checking input file...
   Input file found: inputs/peaks.bed 
   File size: 2.83 KB
   Last modified: 2026-03-30 08:04:47.227267 

4. Reading peaks from BED file...
   Number of peaks loaded: 101 
   Genomic ranges loaded successfully.

5. Annotating peaks with genomic features...
   Using parameters:
   - tssRegion: c(-3000, 3000)
   - TxDb: TxDb.Hsapiens.UCSC.hg19.knownGene
   - annoDb: org.Hs.eg.db

>> preparing features information...		 2026-04-02 04:46:13 AM 
>> Using Genome: hg19 ...
>> identifying nearest features...		 2026-04-02 04:46:15 AM 
>> calculating distance from peak to TSS...	 2026-04-02 04:46:15 AM 
>> assigning genomic annotation...		 2026-04-02 04:46:15 AM 
>> Using Genome: hg19 ...
>> Using Genome: hg19 ...
>> adding gene annotation...			 2026-04-02 04:46:43 AM 
>> assigning chromosome lengths			 2026-04-02 04:46:43 AM 
>> done...					 2026-04-02 04:46:43 AM 
   Peak annotation completed successfully.
   Class of annotation object: csAnno 
   Annotation type: Promoter (<=1kb) ...

6. Saving complete annotation object...
   Saved to: outputs/annotated_peaks.rds 

7. Exporting tabular annotations...
   Columns with NA values:
   - ENSEMBL : 12 NAs ( 11.9 %)
   Tabular data saved to: outputs/peak_annotation.csv 
   Table dimensions: 101 rows × 20 columns

8. Performing quality checks...
   ✓ Both output files created successfully.
     - outputs/annotated_peaks.rds : 5.05 KB
     - outputs/peak_annotation.csv : 20.07 KB

9. Analyzing annotation distribution...
   Annotation category distribution:
   - Promoter (<=1kb): 8.9%
   - Promoter (1-2kb): 4%
   - 3' UTR: 4%
   - 1st Exon: 1%
   - Other Exon: 2%
   - 1st Intron: 23.8%
   - Other Intron: 5.9%
   - Distal Intergenic: 50.5%

   Peaks within ±3kb of TSS: 13 ( 12.9 %)

10. Checking for malformed entries...
   Empty/missing gene symbols: 0 

11. Summary of annotation results:
   Total peaks processed: 101 
   Unique genes annotated: 13 
   Top annotation types:
   - Distal Intergenic: 51 (50.5%)
   - Promoter (<=1kb): 9 (8.9%)
   - 3' UTR: 4 (4%)
   - Intron (ENST00000510175.6_4/255403, intron 1 of 1): 4 (4%)
   - Intron (ENST00000642529.1_1/255403, intron 1 of 2): 4 (4%)

=============================================
Annotation completed successfully!
Output files:
1. outputs/annotated_peaks.rds - Complete csAnno object
2. outputs/peak_annotation.csv - Tabular annotation data
=============================================
```

**`stderr.txt`**

```text

ChIPseeker v1.46.1 Learn more at https://yulab-smu.top/contribution-knowledge-mining/

Please cite:

Qianwen Wang, Ming Li, Tianzhi Wu, Li Zhan, Lin Li, Meijun Chen, Wenqin
Xie, Zijing Xie, Erqiang Hu, Shuangbin Xu, Guangchuang Yu. Exploring
epigenomic datasets by ChIPseeker. Current Protocols. 2022, 2(10): e585

Attaching package: ‘generics’

The following objects are masked from ‘package:base’:

    as.difftime, as.factor, as.ordered, intersect, is.element, setdiff,
    setequal, union


Attaching package: ‘BiocGenerics’

The following objects are masked from ‘package:stats’:

    IQR, mad, sd, var, xtabs

The following objects are masked from ‘package:base’:

    anyDuplicated, aperm, append, as.data.frame, basename, cbind,
    colnames, dirname, do.call, duplicated, eval, evalq, Filter, Find,
    get, grep, grepl, is.unsorted, lapply, Map, mapply, match, mget,
    order, paste, pmax, pmax.int, pmin, pmin.int, Position, rank,
    rbind, Reduce, rownames, sapply, saveRDS, table, tapply, unique,
    unsplit, which.max, which.min


Attaching package: ‘S4Vectors’

The following object is masked from ‘package:utils’:

    findMatches

The following objects are masked from ‘package:base’:

    expand.grid, I, unname

Welcome to Bioconductor

    Vignettes contain introductory material; view with
    'browseVignettes()'. To cite Bioconductor, see
    'citation("Biobase")', and for packages 'citation("pkgname")'.


'select()' returned 1:1 mapping between keys and columns
```

## Biomni Output Files

**`outputs/annotated_peaks.rds`**

```text
[binary file]
size_bytes: 5175
sha256: 339e9e4c4b12fd82bf97e900133ae1ce5b7e032a375ae1a882e99d7b50963830
```

**`outputs/peak_annotation.csv`**

```csv
"seqnames","start","end","width","strand","V4","V5","V6","annotation","geneChr","geneStart","geneEnd","geneLength","geneStrand","geneId","transcriptId","distanceToTSS","ENSEMBL","SYMBOL","GENENAME"
"chr3",198109,198434,326,"*","peak",151,"+","Intron (ENST00000663345.2_6/101927174, intron 1 of 2)",3,237440,238224,785,2,"101927174","ENST00000757007.1_1",39790,NA,"CHL1-AS2","CHL1 antisense RNA 2"
"chr5",147187,147292,106,"*","peak",673,"+","Intron (ENST00000637938.2_8/153478, intron 6 of 19)",5,140681,157225,16545,1,"153478","ENST00000502646.1_3",6506,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr4",28737,28923,187,"*","peak",263,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-24257,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr5",197694,198012,319,"*","peak",382,"+","3' UTR",5,191610,196449,4840,1,"389257","ENST00000328278.4_4",6084,"ENSG00000185028","LRRC14B","leucine rich repeat containing 14B"
"chr3",68590,68842,253,"*","peak",21,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",3159,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr2",178556,178707,152,"*","peak",379,"+","Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4)",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",52452,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr2",186956,187375,420,"*","peak",342,"+","Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4)",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",43784,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr3",104409,104796,388,"*","peak",882,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",38978,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr3",73456,73918,463,"*","peak",193,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",8025,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr2",42434,42718,285,"*","peak",676,"+","Promoter (<=1kb)",2,41220,42952,1733,2,"642273","ENST00000460464.1_3",234,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr1",64426,64659,234,"*","peak",50,"+","Promoter (<=1kb)",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",-760,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr3",60490,60831,342,"*","peak",156,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",-4600,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr2",31626,31786,161,"*","peak",729,"+","Distal Intergenic",2,41220,42952,1733,2,"642273","ENST00000460464.1_3",11166,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr2",167270,167388,119,"*","peak",594,"+","Intron (ENST00000775033.1_2/ENST00000775033.1_2, intron 3 of 3)",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",63771,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr4",9165,9526,362,"*","peak",792,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-43654,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr1",37717,37985,269,"*","peak",563,"+","Promoter (<=1kb)",1,34553,37595,3043,2,"645520","ENST00000834250.1_2",-122,"ENSG00000237613","FAM138A","family with sequence similarity 138 member A"
"chr3",87682,87881,200,"*","peak",851,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",22251,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr1",37567,37954,388,"*","peak",562,"+","Promoter (<=1kb)",1,34553,37595,3043,2,"645520","ENST00000834250.1_2",0,"ENSG00000237613","FAM138A","family with sequence similarity 138 member A"
"chr5",52068,52521,454,"*","peak",403,"+","Exon (ENST00000846714.1_2/ENST00000846714.1_2, exon 2 of 2)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-39762,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr5",47771,47985,215,"*","peak",803,"+","Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 1 of 4)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-44298,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr5",119531,119698,168,"*","peak",672,"+","Intron (ENST00000637938.2_8/153478, intron 2 of 19)",5,140373,190087,49715,1,"153478","ENST00000283426.11_5",-20675,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr4",131980,132105,126,"*","peak",204,"+","Intron (ENST00000510175.6_4/255403, intron 1 of 1)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",7560,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr2",95180,95442,263,"*","peak",761,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-48310,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr4",103830,104031,202,"*","peak",968,"+","Distal Intergenic",4,85621,87340,1720,1,"152687","ENST00000380882.5",18209,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr1",16721,17008,288,"*","peak",916,"+","Promoter (1-2kb)",1,14409,18061,3653,2,"653635","ENST00000831739.1_1",1053,"ENSG00000310526","WASH7P","WASP family homolog 7, pseudogene"
"chr4",164948,165280,333,"*","peak",78,"+","Intron (ENST00000642529.1_1/255403, intron 1 of 2)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",40528,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr5",28844,28996,153,"*","peak",363,"+","Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 2 of 4)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-63287,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr1",38742,39054,313,"*","peak",667,"+","Promoter (1-2kb)",1,34553,37595,3043,2,"645520","ENST00000834250.1_2",-1147,"ENSG00000237613","FAM138A","family with sequence similarity 138 member A"
"chr4",93784,94102,319,"*","peak",127,"+","Distal Intergenic",4,85621,87340,1720,1,"152687","ENST00000380882.5",8163,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr1",196116,196528,413,"*","peak",381,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",-55777,NA,"LOC729737","uncharacterized LOC729737"
"chr2",68926,69106,181,"*","peak",569,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-22056,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr3",79177,79367,191,"*","peak",417,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",13746,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr2",55698,56108,411,"*","peak",89,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-8828,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr5",91238,91494,257,"*","peak",678,"+","Promoter (<=1kb)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-789,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr4",171139,171456,318,"*","peak",108,"+","Intron (ENST00000642529.1_1/255403, intron 1 of 2)",4,206367,249774,43408,1,"642280","ENST00000356347.4_4",-34911,"ENSG00000290382","ZNF876P","zinc finger protein 876, pseudogene"
"chr5",55583,55809,227,"*","peak",871,"+","Intron (ENST00000846515.1_2/ENST00000846515.1_2, intron 1 of 1)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-36474,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr4",140793,141146,354,"*","peak",815,"+","Intron (ENST00000510175.6_4/255403, intron 1 of 1)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",16373,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr2",65231,65663,433,"*","peak",713,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-18361,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr5",67301,67427,127,"*","peak",692,"+","Intron (ENST00000846515.1_2/ENST00000846515.1_2, intron 1 of 1)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-24856,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr3",125856,126284,429,"*","peak",224,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",60425,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr5",8869,9350,482,"*","peak",557,"+","Distal Intergenic",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-82933,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr5",86842,87287,446,"*","peak",275,"+","Distal Intergenic",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-4996,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr1",86895,87073,179,"*","peak",620,"+","Distal Intergenic",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",21476,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr4",16244,16456,213,"*","peak",358,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-36724,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr4",142470,142682,213,"*","peak",520,"+","Intron (ENST00000510175.6_4/255403, intron 1 of 1)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",18050,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr5",20625,20981,357,"*","peak",867,"+","Distal Intergenic",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-71302,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr3",149182,149426,245,"*","peak",332,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",83751,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr2",14230,14335,106,"*","peak",505,"+","Distal Intergenic",2,41220,42952,1733,2,"642273","ENST00000460464.1_3",28617,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr1",115121,115397,277,"*","peak",602,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",24942,NA,"LOC729737","uncharacterized LOC729737"
"chr5",141843,142097,255,"*","peak",710,"+","Promoter (1-2kb)",5,140681,157225,16545,1,"153478","ENST00000502646.1_3",1162,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr2",137194,137461,268,"*","peak",628,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-90324,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr5",181790,181895,106,"*","peak",314,"+","Exon (ENST00000637938.2_8/153478, exon 19 of 20)",5,191610,196449,4840,1,"389257","ENST00000328278.4_4",-9715,"ENSG00000185028","LRRC14B","leucine rich repeat containing 14B"
"chr2",87146,87264,119,"*","peak",770,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-40276,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr4",81106,81356,251,"*","peak",151,"+","Intron (ENST00000608255.2_3/152687, intron 1 of 2)",4,85621,87340,1720,1,"152687","ENST00000380882.5",-4265,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr2",115158,115431,274,"*","peak",727,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-68288,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr1",101110,101294,185,"*","peak",296,"+","Intron (ENST00000833190.1_2/ENST00000833190.1_2, intron 1 of 1)",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",35691,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr5",51138,51305,168,"*","peak",355,"+","Exon (ENST00000846714.1_2/ENST00000846714.1_2, exon 1 of 2)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-40978,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr1",49136,49470,335,"*","peak",198,"+","Distal Intergenic",1,34553,37595,3043,2,"645520","ENST00000834250.1_2",-11541,"ENSG00000237613","FAM138A","family with sequence similarity 138 member A"
"chr4",68971,69214,244,"*","peak",521,"+","Intron (ENST00000608255.2_3/152687, intron 1 of 2)",4,53223,60407,7185,1,"152687","ENST00000502981.2_1",15748,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr1",140050,140515,466,"*","peak",906,"+","Promoter (<=1kb)",1,139790,140339,550,2,"729737","ENST00000493797.1_5",0,NA,"LOC729737","uncharacterized LOC729737"
"chr1",199129,199499,371,"*","peak",801,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",-58790,NA,"LOC729737","uncharacterized LOC729737"
"chr2",177254,177746,493,"*","peak",567,"+","Intron (ENST00000774822.1_2/ENST00000774822.1_2, intron 1 of 4)",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",53413,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr2",38474,38846,373,"*","peak",907,"+","3' UTR",2,41220,42952,1733,2,"642273","ENST00000460464.1_3",4106,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr4",187150,187410,261,"*","peak",615,"+","Intron (ENST00000642529.1_1/255403, intron 1 of 2)",4,206367,249774,43408,1,"642280","ENST00000356347.4_4",-18957,"ENSG00000290382","ZNF876P","zinc finger protein 876, pseudogene"
"chr5",99000,99130,131,"*","peak",730,"+","Intron (ENST00000637938.2_8/153478, intron 1 of 19)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",6717,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr5",39441,39884,444,"*","peak",548,"+","Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 1 of 4)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-52399,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr1",92426,92559,134,"*","peak",317,"+","Distal Intergenic",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",27007,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr5",191861,191994,134,"*","peak",366,"+","Promoter (<=1kb)",5,191610,196449,4840,1,"389257","ENST00000328278.4_4",251,"ENSG00000185028","LRRC14B","leucine rich repeat containing 14B"
"chr1",65448,65771,324,"*","peak",510,"+","Promoter (<=1kb)",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",29,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr1",135324,135583,260,"*","peak",921,"+","3' UTR",1,139790,140339,550,2,"729737","ENST00000493797.1_5",4756,NA,"LOC729737","uncharacterized LOC729737"
"chr2",174666,174813,148,"*","peak",780,"+","Intron (ENST00000774826.1_1/ENST00000774826.1_1, intron 1 of 3)",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",56346,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr3",148400,148825,426,"*","peak",416,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",82969,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr3",40267,40674,408,"*","peak",829,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",-24757,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr4",87379,87633,255,"*","peak",737,"+","Promoter (1-2kb)",4,85621,87340,1720,1,"152687","ENST00000380882.5",1758,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr5",92245,92545,301,"*","peak",560,"+","Promoter (<=1kb)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",0,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr3",124380,124603,224,"*","peak",677,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",58949,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr1",127988,128323,336,"*","peak",161,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",12016,NA,"LOC729737","uncharacterized LOC729737"
"chr1",106401,106756,356,"*","peak",107,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",33583,NA,"LOC729737","uncharacterized LOC729737"
"chr3",33347,33717,371,"*","peak",106,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",-31714,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr3",132315,132464,150,"*","peak",221,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",66884,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr3",83017,83381,365,"*","peak",977,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",17586,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr4",159797,160287,491,"*","peak",663,"+","Intron (ENST00000642529.1_1/255403, intron 1 of 2)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",35377,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr1",135747,136146,400,"*","peak",404,"+","3' UTR",1,139790,140339,550,2,"729737","ENST00000493797.1_5",4193,NA,"LOC729737","uncharacterized LOC729737"
"chr2",27320,27473,154,"*","peak",463,"+","Distal Intergenic",2,41220,42952,1733,2,"642273","ENST00000460464.1_3",15479,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr2",67802,68134,333,"*","peak",736,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-20932,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr1",173392,173695,304,"*","peak",189,"+","Intron (ENST00000466557.2/ENST00000466557.2, intron 1 of 7)",1,139790,140339,550,2,"729737","ENST00000493797.1_5",-33053,NA,"LOC729737","uncharacterized LOC729737"
"chr1",185300,185586,287,"*","peak",788,"+","Distal Intergenic",1,139790,140339,550,2,"729737","ENST00000493797.1_5",-44961,NA,"LOC729737","uncharacterized LOC729737"
"chr4",141743,142067,325,"*","peak",916,"+","Intron (ENST00000510175.6_4/255403, intron 1 of 1)",4,124420,156491,32072,1,"255403","ENST00000609714.1_2",17323,"ENSG00000250312","ZNF718","zinc finger protein 718"
"chr3",20077,20424,348,"*","peak",539,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",-45007,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr4",70167,70588,422,"*","peak",161,"+","Intron (ENST00000608255.2_3/152687, intron 1 of 2)",4,85621,87340,1720,1,"152687","ENST00000380882.5",-15033,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr5",152603,152936,334,"*","peak",535,"+","Intron (ENST00000637938.2_8/153478, intron 7 of 19)",5,140681,157225,16545,1,"153478","ENST00000502646.1_3",11922,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr5",83576,83802,227,"*","peak",219,"+","Distal Intergenic",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-8481,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr4",7178,7328,151,"*","peak",912,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-45852,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr3",55841,56248,408,"*","peak",473,"+","Distal Intergenic",3,65431,66175,745,1,"102723448","ENST00000440867.1",-9183,"ENSG00000223587","LINC01986","long intergenic non-protein coding RNA 1986"
"chr5",29507,29931,425,"*","peak",342,"+","Intron (ENST00000846370.1_1/ENST00000846370.1_1, intron 2 of 4)",5,92283,190081,97799,1,"153478","ENST00000637938.2_8",-62352,"ENSG00000153404","PLEKHG4B","pleckstrin homology and RhoGEF domain containing G4B"
"chr2",93228,93641,414,"*","peak",735,"+","Distal Intergenic",2,41221,46870,5650,2,"642273","ENST00000461026.1_3",-46358,"ENSG00000184731","FAM110C","family with sequence similarity 110 member C"
"chr3",181252,181715,464,"*","peak",312,"+","Intron (ENST00000663345.2_6/101927174, intron 1 of 2)",3,237440,238224,785,2,"101927174","ENST00000757007.1_1",56509,NA,"CHL1-AS2","CHL1 antisense RNA 2"
"chr1",88650,89146,497,"*","peak",20,"+","Distal Intergenic",1,65419,71585,6167,1,"79501","ENST00000641515.2_6",23231,"ENSG00000186092","OR4F5","olfactory receptor family 4 subfamily F member 5"
"chr2",139284,139536,253,"*","peak",578,"+","Distal Intergenic",2,222361,231159,8799,2,"26751","ENST00000472012.1_3",91623,"ENSG00000035115","SH3YL1","SH3 and SYLF domain containing 1"
"chr4",22481,22958,478,"*","peak",231,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-30222,"ENSG00000272602","ZNF595","zinc finger protein 595"
"chr4",9850,10161,312,"*","peak",463,"+","Distal Intergenic",4,53180,87412,34233,1,"152687","ENST00000608255.2_3",-43019,"ENSG00000272602","ZNF595","zinc finger protein 595"
```

## Biomni Metadata

```json
{
  "task_id": "chipseeker/H001_annotate_peaks",
  "package": "chipseeker",
  "track_id": "omics_core",
  "content_tag_id": "omics",
  "flow_tag_id": "report",
  "scoring_mode_id": "strict",
  "code_sha256": "fc2ade8cf7eeafe0b7d1a4f2a5d5861cd53d9c277a4fefb570d9182f527aaca0",
  "agent": "biomni",
  "model": "deepseek/deepseek-v3.2-exp",
  "temperature": 1.0,
  "timestamp": "2026-04-02T13:46:05.549268",
  "raw_response": "",
  "token_usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  },
  "gen_time_seconds": 104.09
}
```

## Evaluation Record

```json
{
  "task_id": "chipseeker/H001_annotate_peaks",
  "sample_idx": 0,
  "agent": "biomni",
  "status": "FAIL",
  "message": "Failed at case_01_seed_1000",
  "timestamp": "2026-02-14T09:56:29.910730",
  "gen_time": 46.32,
  "docker_time": 97.01,
  "test_cases": [
    {
      "case": "case_01_seed_1000",
      "status": "FAIL",
      "comparison": {
        "peak_annotation.csv": {
          "match": false,
          "reason": "Comparison error: Error tokenizing data. C error: Expected 21 fields in line 36, saw 22\n"
        },
        "annotated_peaks.rds": {
          "match": true
        }
      },
      "returncode": 0
    }
  ]
}
```
