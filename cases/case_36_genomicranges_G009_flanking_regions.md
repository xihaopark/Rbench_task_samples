# Case 36 - `genomicranges/G009_flanking_regions`
**Track:** `omics_core`  **Package:** `genomicranges`  **Function:** `flank`  **Level:** `L2`  **Agent sample:** Biomni `sample_01`  **Evaluation status:** `NO_OUTPUT`
**Evaluation message:** Failed at case_01_seed_1000
**Sample status counts:** `{"NO_OUTPUT": 4, "PASS": 1}`

## Task Prompt

```text
Write R code to extract 500 bp upstream flanking regions around genomic intervals using GenomicRanges. At the beginning, load the required packages: library(GenomicRanges). These upstream flanks are often enriched for promoters and transcription factor binding sites, so we want to define them precisely starting from the interval annotations stored in inputs/intervals.csv. Read the CSV, convert the intervals into a GRanges object using only GenomicRanges and its documented helper utilities, then apply the flank() function with width set to 500 and both set to FALSE to obtain the upstream regions, and finally save the resulting GRanges object as an RDS file at outputs/flanks.rds. Please rely solely on GenomicRanges without introducing additional toolkits, and as a quick quality check make sure outputs/flanks.rds is created, inspect a handful of records to confirm strand-aware coordinates look reasonable, and verify there are no unexpected NAs or clearly mispositioned flanks.
```

## Input Files

**`inputs/genes.csv`**

```csv
chr,start,end,score,strand,gene
chr4,28211,28533,0.866381723553756,-,GENE53
chr1,10762,11024,0.41071467794910366,-,GENE66
chr2,14851,14960,0.674834161084158,-,GENE47
chr4,47853,47910,0.06908386128849087,+,GENE43
chr4,83717,83891,0.8815135658569732,-,GENE34
chr5,74718,75031,0.7347616410878752,+,GENE67
chr4,52156,52304,0.6637256923961905,-,GENE44
chr5,79617,79740,0.6791475204846237,+,GENE19
chr3,90940,91081,0.4577340419401681,-,GENE72
chr4,43856,44009,0.18150175729153661,-,GENE73
chr3,30477,30947,0.4430202106050787,+,GENE4
chr4,34625,34826,0.5870864444429019,+,GENE25
chr3,82561,82783,0.4116004485556236,+,GENE46
chr5,28154,28499,0.3076700911914664,-,GENE56
chr1,19776,20186,0.8705937045392624,-,GENE48
chr5,22751,22885,0.3628622290316542,+,GENE3
chr3,26405,26767,0.5578259687986639,-,GENE39
chr1,85641,85712,0.7078104353505493,-,GENE55
chr2,6326,6462,0.0491650688963271,-,GENE6
chr2,67808,68003,0.36089498796242003,+,GENE9
chr2,71067,71363,0.2136893007199293,-,GENE70
chr4,1285,1733,0.2835088652286557,+,GENE2
chr2,44123,44580,0.5904466122684152,-,GENE37
chr3,57199,57680,0.17128328169110885,-,GENE8
chr1,98852,98961,0.6220396607099883,+,GENE24
chr5,16235,16298,0.3727541139840933,-,GENE33
chr5,19191,19439,0.559342885108253,+,GENE38
chr3,34814,35239,0.01022172144268807,-,GENE79
chr5,5061,5175,0.6735437037855273,-,GENE35
chr2,73725,74134,0.5833154907769438,-,GENE22
chr3,57792,58018,0.1525636249070338,-,GENE75
chr1,17444,17781,0.5031339678424274,+,GENE17
chr1,38072,38328,0.12229893063219277,-,GENE15
chr1,57773,58062,0.09878050027245322,+,GENE69
chr1,93510,93976,0.8128719264108901,-,GENE27
chr5,47158,47532,0.7110646243239135,-,GENE49
chr1,50803,51098,0.21124045958996895,-,GENE76
chr1,33983,34357,0.1904835268737184,+,GENE59
chr2,45891,46009,0.5006341953590157,+,GENE54
chr3,32553,32945,0.6698593402147363,-,GENE31
chr5,40851,41251,0.9155562563767196,-,GENE74
chr1,7581,7691,0.6741459794705988,-,GENE68
chr4,14798,15152,0.4695706953090436,+,GENE23
chr3,54887,55215,0.7710289733524976,+,GENE16
chr3,71613,71869,0.4367624727025651,-,GENE7
chr3,24946,25281,0.7330201520435458,+,GENE78
chr5,89331,89770,0.12849662716458166,+,GENE26
chr1,70545,70785,0.14262783498704945,+,GENE57
chr2,30595,30831,0.3762522349731179,-,GENE32
chr2,98067,98525,0.2166026261842715,+,GENE50
```

**`inputs/intervals.csv`**

```csv
chr,start,end,score,strand,gene
chr3,56310,56674,0.9561320219245817,+,GENE0
chr5,75228,75726,0.199429237951247,-,GENE1
chr4,1285,1733,0.2835088652286557,+,GENE2
chr5,22751,22885,0.3628622290316542,+,GENE3
chr3,30477,30947,0.4430202106050787,+,GENE4
chr2,1865,2136,0.42059962460491607,+,GENE5
chr2,6326,6462,0.0491650688963271,-,GENE6
chr3,71613,71869,0.4367624727025651,-,GENE7
chr3,57199,57680,0.17128328169110885,-,GENE8
chr2,67808,68003,0.36089498796242003,+,GENE9
chr1,94115,94468,0.6796249581769924,-,GENE10
chr3,86076,86518,0.6831573755440192,+,GENE11
chr2,72703,73086,0.07902451357882101,+,GENE12
chr2,49122,49260,0.0852532444662456,+,GENE13
chr4,85781,86026,0.5605097587889222,+,GENE14
chr1,38072,38328,0.12229893063219277,-,GENE15
chr3,54887,55215,0.7710289733524976,+,GENE16
chr1,17444,17781,0.5031339678424274,+,GENE17
chr5,38585,38873,0.5900257640311124,-,GENE18
chr5,79617,79740,0.6791475204846237,+,GENE19
chr5,60838,61184,0.664249361522212,-,GENE20
chr4,99059,99294,0.7524690926022803,-,GENE21
chr2,73725,74134,0.5833154907769438,-,GENE22
chr4,14798,15152,0.4695706953090436,+,GENE23
chr1,98852,98961,0.6220396607099883,+,GENE24
chr4,34625,34826,0.5870864444429019,+,GENE25
chr5,89331,89770,0.12849662716458166,+,GENE26
chr1,93510,93976,0.8128719264108901,-,GENE27
chr4,52444,52812,0.910626853067677,-,GENE28
chr1,37045,37138,0.383191987172398,+,GENE29
chr2,21612,21818,0.5302675783042549,-,GENE30
chr3,32553,32945,0.6698593402147363,-,GENE31
chr2,30595,30831,0.3762522349731179,-,GENE32
chr5,16235,16298,0.3727541139840933,-,GENE33
chr4,83717,83891,0.8815135658569732,-,GENE34
chr5,5061,5175,0.6735437037855273,-,GENE35
chr4,19266,19524,0.14824987599649286,-,GENE36
chr2,44123,44580,0.5904466122684152,-,GENE37
chr5,19191,19439,0.559342885108253,+,GENE38
chr3,26405,26767,0.5578259687986639,-,GENE39
chr5,24267,24365,0.8019425462459494,+,GENE40
chr5,59967,60037,0.19678587970995576,-,GENE41
chr1,66160,66465,0.9677151764648408,-,GENE42
chr4,47853,47910,0.06908386128849087,+,GENE43
chr4,52156,52304,0.6637256923961905,-,GENE44
chr5,8820,9117,0.37511912386841206,-,GENE45
chr3,82561,82783,0.4116004485556236,+,GENE46
chr2,14851,14960,0.674834161084158,-,GENE47
chr1,19776,20186,0.8705937045392624,-,GENE48
chr5,47158,47532,0.7110646243239135,-,GENE49
chr2,98067,98525,0.2166026261842715,+,GENE50
chr5,34792,35050,0.26834409650242885,-,GENE51
chr2,39891,40091,0.35162802427465756,+,GENE52
chr4,28211,28533,0.866381723553756,-,GENE53
chr2,45891,46009,0.5006341953590157,+,GENE54
chr1,85641,85712,0.7078104353505493,-,GENE55
chr5,28154,28499,0.3076700911914664,-,GENE56
chr1,70545,70785,0.14262783498704945,+,GENE57
chr4,32953,33116,0.2898657654236073,-,GENE58
chr1,33983,34357,0.1904835268737184,+,GENE59
chr1,63114,63562,0.905075098973956,-,GENE60
chr2,4914,5093,0.5632787853943745,+,GENE61
chr2,43705,43832,0.6117005902125847,-,GENE62
chr4,43731,43810,0.5440983271058021,-,GENE63
chr5,8583,8817,0.3602251879196178,-,GENE64
chr5,71379,71544,0.920661185520118,-,GENE65
chr1,10762,11024,0.41071467794910366,-,GENE66
chr5,74718,75031,0.7347616410878752,+,GENE67
chr1,7581,7691,0.6741459794705988,-,GENE68
chr1,57773,58062,0.09878050027245322,+,GENE69
chr2,71067,71363,0.2136893007199293,-,GENE70
chr3,68754,69156,0.6604303389270132,-,GENE71
chr3,90940,91081,0.4577340419401681,-,GENE72
chr4,43856,44009,0.18150175729153661,-,GENE73
chr5,40851,41251,0.9155562563767196,-,GENE74
chr3,57792,58018,0.1525636249070338,-,GENE75
chr1,50803,51098,0.21124045958996895,-,GENE76
chr1,25942,26135,0.4677544550298979,+,GENE77
chr3,24946,25281,0.7330201520435458,+,GENE78
chr3,34814,35239,0.01022172144268807,-,GENE79
```

**`inputs/query.csv`**

```csv
chr,start,end,score,strand,gene
chr3,56310,56674,0.9561320219245817,+,GENE0
chr5,75228,75726,0.199429237951247,-,GENE1
chr4,1285,1733,0.2835088652286557,+,GENE2
chr5,22751,22885,0.3628622290316542,+,GENE3
chr3,30477,30947,0.4430202106050787,+,GENE4
chr2,1865,2136,0.42059962460491607,+,GENE5
chr2,6326,6462,0.0491650688963271,-,GENE6
chr3,71613,71869,0.4367624727025651,-,GENE7
chr3,57199,57680,0.17128328169110885,-,GENE8
chr2,67808,68003,0.36089498796242003,+,GENE9
chr1,94115,94468,0.6796249581769924,-,GENE10
chr3,86076,86518,0.6831573755440192,+,GENE11
chr2,72703,73086,0.07902451357882101,+,GENE12
chr2,49122,49260,0.0852532444662456,+,GENE13
chr4,85781,86026,0.5605097587889222,+,GENE14
chr1,38072,38328,0.12229893063219277,-,GENE15
chr3,54887,55215,0.7710289733524976,+,GENE16
chr1,17444,17781,0.5031339678424274,+,GENE17
chr5,38585,38873,0.5900257640311124,-,GENE18
chr5,79617,79740,0.6791475204846237,+,GENE19
chr5,60838,61184,0.664249361522212,-,GENE20
chr4,99059,99294,0.7524690926022803,-,GENE21
chr2,73725,74134,0.5833154907769438,-,GENE22
chr4,14798,15152,0.4695706953090436,+,GENE23
chr1,98852,98961,0.6220396607099883,+,GENE24
chr4,34625,34826,0.5870864444429019,+,GENE25
chr5,89331,89770,0.12849662716458166,+,GENE26
chr1,93510,93976,0.8128719264108901,-,GENE27
chr4,52444,52812,0.910626853067677,-,GENE28
chr1,37045,37138,0.383191987172398,+,GENE29
chr2,21612,21818,0.5302675783042549,-,GENE30
chr3,32553,32945,0.6698593402147363,-,GENE31
chr2,30595,30831,0.3762522349731179,-,GENE32
chr5,16235,16298,0.3727541139840933,-,GENE33
chr4,83717,83891,0.8815135658569732,-,GENE34
chr5,5061,5175,0.6735437037855273,-,GENE35
chr4,19266,19524,0.14824987599649286,-,GENE36
chr2,44123,44580,0.5904466122684152,-,GENE37
chr5,19191,19439,0.559342885108253,+,GENE38
chr3,26405,26767,0.5578259687986639,-,GENE39
```

**`inputs/subject.csv`**

```csv
chr,start,end,score,strand,gene
chr5,24267,24365,0.8019425462459494,+,GENE40
chr5,59967,60037,0.19678587970995576,-,GENE41
chr1,66160,66465,0.9677151764648408,-,GENE42
chr4,47853,47910,0.06908386128849087,+,GENE43
chr4,52156,52304,0.6637256923961905,-,GENE44
chr5,8820,9117,0.37511912386841206,-,GENE45
chr3,82561,82783,0.4116004485556236,+,GENE46
chr2,14851,14960,0.674834161084158,-,GENE47
chr1,19776,20186,0.8705937045392624,-,GENE48
chr5,47158,47532,0.7110646243239135,-,GENE49
chr2,98067,98525,0.2166026261842715,+,GENE50
chr5,34792,35050,0.26834409650242885,-,GENE51
chr2,39891,40091,0.35162802427465756,+,GENE52
chr4,28211,28533,0.866381723553756,-,GENE53
chr2,45891,46009,0.5006341953590157,+,GENE54
chr1,85641,85712,0.7078104353505493,-,GENE55
chr5,28154,28499,0.3076700911914664,-,GENE56
chr1,70545,70785,0.14262783498704945,+,GENE57
chr4,32953,33116,0.2898657654236073,-,GENE58
chr1,33983,34357,0.1904835268737184,+,GENE59
chr1,63114,63562,0.905075098973956,-,GENE60
chr2,4914,5093,0.5632787853943745,+,GENE61
chr2,43705,43832,0.6117005902125847,-,GENE62
chr4,43731,43810,0.5440983271058021,-,GENE63
chr5,8583,8817,0.3602251879196178,-,GENE64
chr5,71379,71544,0.920661185520118,-,GENE65
chr1,10762,11024,0.41071467794910366,-,GENE66
chr5,74718,75031,0.7347616410878752,+,GENE67
chr1,7581,7691,0.6741459794705988,-,GENE68
chr1,57773,58062,0.09878050027245322,+,GENE69
chr2,71067,71363,0.2136893007199293,-,GENE70
chr3,68754,69156,0.6604303389270132,-,GENE71
chr3,90940,91081,0.4577340419401681,-,GENE72
chr4,43856,44009,0.18150175729153661,-,GENE73
chr5,40851,41251,0.9155562563767196,-,GENE74
chr3,57792,58018,0.1525636249070338,-,GENE75
chr1,50803,51098,0.21124045958996895,-,GENE76
chr1,25942,26135,0.4677544550298979,+,GENE77
chr3,24946,25281,0.7330201520435458,+,GENE78
chr3,34814,35239,0.01022172144268807,-,GENE79
```

## Reference Code

```r
#!/usr/bin/env Rscript
library(GenomicRanges)
df <- read.csv('inputs/intervals.csv')
gr <- makeGRangesFromDataFrame(
  df,
  seqnames.field = 'chr',
  start.field = 'start',
  end.field = 'end',
  strand.field = 'strand',
  keep.extra.columns = TRUE
)
flanks = flank(gr, width=500, both=FALSE)
saveRDS(flanks, 'outputs/flanks.rds')
```

## Reference Output

**`outputs/flanks.rds`**

```text
[binary file]
size_bytes: 1825
sha256: 3f0942fb7e725d427a6c1e50ef1bc1c673367dd8027533aa560924d28d64a73e
```

## Biomni Code

```r
#!/usr/bin/env Rscript

# Load required package
library(GenomicRanges)

# Create outputs directory if it doesn't exist
dir.create("outputs", showWarnings = FALSE)

# Read the intervals from CSV file
intervals_df <- read.csv("inputs/intervals.csv")

# Convert to GRanges object
# Note: We need to ensure strand is properly formatted
intervals_gr <- GRanges(
    seqnames = intervals_df$seqnames,
    ranges = IRanges(start = intervals_df$start, end = intervals_df$end),
    strand = intervals_df$strand,
    gene = intervals_df$gene
)

# Extract 500 bp upstream flanking regions
# flank() with both=FALSE gives upstream regions
# For + strand: upstream is before start
# For - strand: upstream is after end
# For * strand: both sides (treated as +)
upstream_flanks <- flank(intervals_gr, width = 500, both = FALSE)

# Save the result as RDS file
saveRDS(upstream_flanks, file = "outputs/flanks.rds")

# Quality checks
cat("=== QUALITY CHECKS ===\n")
cat("1. Checking if output file exists:\n")
if (file.exists("outputs/flanks.rds")) {
    cat("   ✓ outputs/flanks.rds created successfully\n")
} else {
    cat("   ✗ outputs/flanks.rds NOT created\n")
}

# Load and inspect the saved object
flanks_loaded <- readRDS("outputs/flanks.rds")

cat("\n2. Basic information about the flanks:\n")
cat("   Number of regions:", length(flanks_loaded), "\n")
cat("   Number of columns in mcols:", ncol(mcols(flanks_loaded)), "\n")

cat("\n3. Checking for NAs in coordinates:\n")
cat("   NAs in seqnames:", sum(is.na(seqnames(flanks_loaded))), "\n")
cat("   NAs in start:", sum(is.na(start(flanks_loaded))), "\n")
cat("   NAs in end:", sum(is.na(end(flanks_loaded))), "\n")
cat("   NAs in strand:", sum(is.na(strand(flanks_loaded))), "\n")

cat("\n4. First 5 flanking regions:\n")
print(head(flanks_loaded, 5))

cat("\n5. Checking strand-aware positioning:\n")
# For + strand: upstream should be before start (start - width to start - 1)
# For - strand: upstream should be after end (end + 1 to end + width)
plus_strand <- flanks_loaded[strand(flanks_loaded) == "+"]
minus_strand <- flanks_loaded[strand(flanks_loaded) == "-"]

if (length(plus_strand) > 0) {
    cat("   For + strand regions, flank should end at original start - 1\n")
    original_plus <- intervals_gr[strand(intervals_gr) == "+"]
    # Check if flank end == original start - 1
    mismatches <- sum(end(plus_strand) != start(original_plus) - 1)
    cat("   Mismatches in + strand positioning:", mismatches, "\n")
}

if (length(minus_strand) > 0) {
    cat("   For - strand regions, flank should start at original end + 1\n")
    original_minus <- intervals_gr[strand(intervals_gr) == "-"]
    # Check if flank start == original end + 1
    mismatches <- sum(start(minus_strand) != end(original_minus) + 1)
    cat("   Mismatches in - strand positioning:", mismatches, "\n")
}

cat("\n6. All flank widths should be 500 bp:\n")
widths <- width(flanks_loaded)
if (all(widths == 500)) {
    cat("   ✓ All flanks have width 500 bp\n")
} else {
    cat("   ✗ Some flanks don't have width 500 bp\n")
    cat("   Unique widths found:", unique(widths), "\n")
}

cat("\n=== QUALITY CHECKS COMPLETE ===\n")
```

## Biomni Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Loading required package: stats4
Loading required package: BiocGenerics
Loading required package: generics

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

Loading required package: S4Vectors

Attaching package: ‘S4Vectors’

The following object is masked from ‘package:utils’:

    findMatches

The following objects are masked from ‘package:base’:

    expand.grid, I, unname

Loading required package: IRanges
Loading required package: Seqinfo
Error in stop_if_wrong_length("'seqnames'", ans_len) : 
  'seqnames' must have the length of the object to construct (80) or length 1
Calls: GRanges -> new_GRanges -> stop_if_wrong_length
Execution halted
```

## Biomni Output Files

_No files available._

## Biomni Metadata

```json
{
  "task_id": "genomicranges/G009_flanking_regions",
  "package": "genomicranges",
  "track_id": "omics_core",
  "content_tag_id": "omics",
  "flow_tag_id": "read",
  "scoring_mode_id": "strict",
  "code_sha256": "595f1115b8905eb07179ce5b4dd440e712907a3f0ccefa1b49d9d556c1eb3f1e",
  "agent": "biomni",
  "model": "deepseek/deepseek-v3.2-exp",
  "temperature": 1.0,
  "timestamp": "2026-04-02T15:08:24.111521",
  "raw_response": "",
  "token_usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  },
  "gen_time_seconds": 132.03
}
```

## Evaluation Record

```json
{
  "task_id": "genomicranges/G009_flanking_regions",
  "sample_idx": 1,
  "agent": "biomni",
  "status": "NO_OUTPUT",
  "message": "Failed at case_01_seed_1000",
  "timestamp": "2026-02-14T12:47:32.153850",
  "gen_time": 41.58,
  "docker_time": 14.8,
  "test_cases": [
    {
      "case": "case_01_seed_1000",
      "status": "NO_OUTPUT",
      "message": "No output files created",
      "stderr": "Loading required package: stats4\nLoading required package: BiocGenerics\nLoading required package: generics\n\nAttaching package: ‘generics’\n\nThe following objects are masked from ‘package:base’:\n\n    as.difftime, as.factor, as.ordered, intersect, is.element, setdiff,\n    setequal, union\n\n\nAttaching package: ‘BiocGenerics’\n\nThe following objects are masked from ‘package:stats’:\n\n    IQR, mad, sd, var, xtabs\n\nThe following objects are masked from ‘package:base’:\n\n    anyDuplicated, aperm, append, as.data.frame, basename, cbind,\n    colnames, dirname, do.call, duplicated, eval, evalq, Filter, Find,\n    get, grep, grepl, is.unsorted, lapply, Map, mapply, match, mget,\n    order, paste, pmax, pmax.int, pmin, pmin.int, Position, rank,\n    rbind, Reduce, rownames, sapply, saveRDS, table, tapply, unique,\n    unsplit, which.max, which.min\n\nLoading required package: S4Vectors\n\nAttaching package: ‘S4Vectors’\n\nThe following object is masked from ‘package:utils’:\n\n    findMatches\n\nThe following object",
      "returncode": 1
    }
  ]
}
```
