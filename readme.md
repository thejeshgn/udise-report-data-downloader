## Source
- [UDISE+ Public Reports](https://dashboard.udiseplus.gov.in/#/reportDashboard/sReport)

## Credit
- You can credit Thejesh GN and link to https://thejeshgn.com

## School Related Datasets
### Columns

- cat1 - PS (I-V)
- cat2 - UPS (I - VIII)
- cat3 - HSS (I - XII)
- cat4 - UPS (VI - VIII)
- cat5 - HSS (VI - XII)
- cat6 - SS (I - X)
- cat7 - SS (VI - X)
- cat8 - SS (IX - X)
- cat9 - ignore
- cat10 - HSS (IX - XII)
- cat11 - HSS (XI - XII)
- Total - Total
- sch_mgmt_id = id school management type
- sch_mgmt_name = name of school management type

## Student Related Datasets

### Columns

### Example Rate Calculation

```pri_girls_repetitionRate = (pri_girl_c1_c5_current_rptr/pri_girl_c1_c5_previous) * 100```

```pri_girls_promotionRate  =  (pri_girl_c2_c6_current_fresh/pri_girl_c1_c5_previous) * 100```

```pri_girls_dropoutRate    = (100 - (pri_girls_promotionRate + pri_girls_repetitionRate)```
