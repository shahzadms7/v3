$BASE = 'https://govrag-v3-func.azurewebsites.net'

function Test-Career {
    param($label, $country, $industry, $resume, $jd)
    $body = ConvertTo-Json @{ resume=$resume; job_description=$jd; country=$country; industry=$industry }
    $err = $null
    $r = $null
    try {
        $r = Invoke-WebRequest -Uri "$BASE/career" -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing -TimeoutSec 120
    }
    catch {
        $err = $_.Exception.Message
    }
    if ($err) {
        Write-Host "[FAIL] $label -- $err" -ForegroundColor Red
        return
    }
    $d = ConvertFrom-Json $r.Content
    $score = $d.naked_truth.composite_score
    $cards = ($d.cards | Get-Member -MemberType NoteProperty).Count
    $qaCount = 0
    if ($d.cards.interviewPrep -and $d.cards.interviewPrep.qa) { $qaCount = $d.cards.interviewPrep.qa.Count }
    $starCount = 0
    if ($d.cards.starStories) { $starCount = $d.cards.starStories.Count }
    $tools = 0
    if ($d.cards.skillsGap -and $d.cards.skillsGap.tools_platforms) { $tools = $d.cards.skillsGap.tools_platforms.Count }
    $atsM = 0
    if ($d.cards.skillsGap.ats_keywords_matched) { $atsM = $d.cards.skillsGap.ats_keywords_matched.Count }
    $atsX = 0
    if ($d.cards.skillsGap.ats_keywords_missing) { $atsX = $d.cards.skillsGap.ats_keywords_missing.Count }
    $certs = 0
    if ($d.cards.skillsGap.certs_to_pursue) { $certs = $d.cards.skillsGap.certs_to_pursue.Count }
    $train = 0
    if ($d.cards.skillsGap.training_resources) { $train = $d.cards.skillsGap.training_resources.Count }
    $trends = 0
    if ($d.cards.skillsGap.emerging_trends) { $trends = $d.cards.skillsGap.emerging_trends.Count }
    $simOcc = "NONE"
    if ($d.similar_occupations) { $simOcc = ($d.similar_occupations -join ' | ') }
    $salary = "MISSING"
    if ($d.cards.salaryNegotiation -and $d.cards.salaryNegotiation.table) { $salary = $d.cards.salaryNegotiation.table[0].range }
    $visa = 0
    if ($d.cards.visaPathways -and $d.cards.visaPathways.outside_country) { $visa = $d.cards.visaPathways.outside_country.Count }
    $provider = $d.ai_provider
    $latency = [int]($d.metrics.latency_ms / 1000)
    $pass = ($qaCount -eq 5) -and ($starCount -eq 3) -and ($tools -ge 5) -and ($cards -ge 15)
    if ($pass) {
        Write-Host "[PASS] $label | Score:$score | $provider | ${latency}s" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $label | Score:$score | $provider | ${latency}s" -ForegroundColor Red
    }
    Write-Host "  Cards:$cards | Q&A:$qaCount/5 | Stars:$starCount/3 | Tools:$tools | ATS+:$atsM ATS-:$atsX"
    Write-Host "  Certs:$certs | Training:$train | Trends:$trends | Visa routes:$visa"
    Write-Host "  Salary entry: $salary"
    Write-Host "  Similar Occs: $simOcc"
    Write-Host ""
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host " ALFALAH AI -- SDLC FULL TEST -- 5 Countries" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

$r1 = "John Smith | Software Engineer | 5 years | Toronto Canada. Skills: Python, JavaScript, React, Node.js, PostgreSQL, Docker, Git, AWS. Led team of 4 to deliver e-commerce platform (50k users). Reduced API latency 40%. Built CI/CD pipeline from 2hrs to 15min. B.Sc. Computer Science University of Toronto 2019. AWS Solutions Architect Associate 2023."
$j1 = "Senior Software Engineer | Toronto Canada | Shopify. Requirements: 5+ years Python/React, AWS, Docker, Kubernetes, microservices, REST APIs, Agile/Scrum. Tech lead experience preferred."
Test-Career "Canada-SoftwareEngineer" "Canada" "Information Technology" $r1 $j1

$r2 = "Sarah Johnson | Registered Nurse | 8 years | London UK. Skills: ICU care, patient assessment, IV therapy, Epic EHR, medication administration, triage. ICU nurse Royal London Hospital. Led triage team 12 nurses COVID-19 surge, zero medication errors 18 months. Implemented handover protocol reducing errors 35%. BScN Manchester 2016. NMC Registration, BLS, ACLS."
$j2 = "Senior Registered Nurse | NHS England London UK. NMC registration required, 5+ years acute care, ICU, Epic EHR, ACLS. Team leadership required."
Test-Career "UK-RegisteredNurse" "United Kingdom" "Healthcare" $r2 $j2

$r3 = "Ahmed Al-Rashidi | Civil Engineer | 6 years | Dubai UAE. Skills: AutoCAD, Revit, BIM, structural analysis, project management, concrete design, FIDIC contracts. Dubai Metro Red Line Extension structural design team of 8, AED 180M. Abu Dhabi Sheikh Zayed Road widening delivered 3 months early AED 270M. PE License UAE 2021. B.Eng Civil Engineering American University Dubai 2018."
$j3 = "Senior Civil Engineer | AECOM Dubai UAE. PE license UAE required, 5+ years Gulf infrastructure, AutoCAD, Revit, BIM 360, PMP preferred. Arabic English bilingual."
Test-Career "UAE-CivilEngineer" "United Arab Emirates" "Engineering" $r3 $j3

$r4 = "Emma Richardson | Financial Analyst | 4 years | Sydney Australia. Skills: Financial modeling, DCF valuation, Excel, Bloomberg Terminal, SQL, Power BI, IFRS. Equity research ASX mining sector AUD 12B portfolio. Built DCF models reducing analysis time 60%. 45 research reports 78% accuracy. B.Com Finance University Sydney 2020. CFA Level 2 candidate."
$j4 = "Senior Financial Analyst | Macquarie Group Sydney Australia. CFA preferred, 4+ years equity research or investment banking, Excel modeling, Bloomberg, Power BI. APRA-regulated environment."
Test-Career "Australia-FinancialAnalyst" "Australia" "Finance" $r4 $j4

$r5 = "Raj Patel | Data Scientist | 1 year | San Francisco USA. Skills: Python, Pandas, Scikit-learn, TensorFlow, SQL, Tableau. Built churn prediction model 87% accuracy 50k users. A/B tested 3 features drove 12% conversion improvement. M.S. Data Science Stanford 2024. Kaggle top 15% NLP competition."
$j5 = "Data Scientist | Google Mountain View CA USA. Python, TensorFlow, ML pipeline, 2+ years preferred, GCP/AWS, distributed computing."
Test-Career "USA-DataScientist" "United States" "Information Technology" $r5 $j5

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host " TEST COMPLETE" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
