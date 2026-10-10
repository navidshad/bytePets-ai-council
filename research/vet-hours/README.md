# Vet hours — call sheet (task C2)

The vet register (VMVT, data.gov.lt set 5258) has no opening hours. This folder holds the sheet we use to phone clinics and write the hours down. Track A imports it (A2).

**Status on 2026-10-10: no clinic has been phoned yet.** Every `checked_on` cell is empty. The columns are a draft to agree with Navid before calling.

## Files

| File | What it is |
|---|---|
| `vilnius-vet-hours.xlsx` | The working sheet: tab **Vets** (47 places) and tab **How to fill** (formats, call script in Lithuanian and English, progress count, sources) |
| `vilnius-vet-hours.csv` | The **Vets** tab as CSV, for import and for reading diffs |

If you edit the sheet, export the Vets tab to the CSV again so the two match.

## What is in it

- **38 places from the VMVT register**, pulled 2026-10-10: 31 vet clinics and 7 retail vet pharmacies in Vilnius city, all with status active. Name, address, phone and coordinates come from the register.
- **9 clinics found on the web** that are not in the register extract (ids `man_…`): four 8 drambliai sites, two VilniusVet branches, Veta, Partnervetas, BioPlanet, Veterinarinė profilaktika. Their legal names and addresses come from clinic websites and the medicina.lt directory, not the register.
- **Left out:** the 2 entries the register marks as suspended, plus wholesalers, a manufacturer and livestock operators. Emails are left out on purpose.

## Hours: what is real and what is not

- **Only 5 rows have hours**, copied from the clinics' own websites on 2026-10-10: 8 drambliai Pavilnys (open 24 hours a day, Tolimoji g. 2B), Antakalnis (08:00–24:00), Naujamiestis (07:00–23:00), Pilaitė (08:00–21:00) and Begemotas (08:00–22:00). They are marked in the `hours_source` column as not checked by phone.
- **The other 42 rows have no hours.**
- **`checked_on` means a person at the clinic confirmed the hours by phone.** A website is not a check. Do not show "checked on [date]" in the app for a row whose `checked_on` is empty.

## Things to confirm on every call

- The register often holds the legal name and legal address, not the name on the door. Three clinics show a different address on the web (Rekso gydykla, VetBalsas, Užupio veterinarijos klinika); see `web_hint_unverified`.
- Three entries registered as pharmacies look like clinics too (VilniusVet Žvėrynas, Jeruzalės / Dr.Vet, Jakovo).
- Four entries are registered as service providers at a flat address and may be visiting vets with no clinic.

## Not complete

The medicina.lt directory lists 82 vet companies for Vilnius. Only its first page was read, so some clinics are missing.

## Sources

- VMVT register: data.gov.lt dataset 5258, `okis_subjektai/Subjektas` (CC BY 4.0)
- Clinic websites read 2026-10-10: 8drambliai.lt, begevet.lt, vilniusvet.lt, drvet.lt, veterinarijavilniuje.lt, veterinarija.eu
- Directory: medicina.lt, veterinary clinics in Vilnius (first page)
