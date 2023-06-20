## Jobs Scraping Project
projekt se snaží scrapovat z populárních webů na pracovní pozice (teď jsou odkazy navoleny tak že tam je cokoliv s daty -> anlytik, scientist, engineer atd.),
bohužel pořádně funguje jen jobs.cz, jinak je to bída. startupjobs.cz funguje lokálně a šlo by nacpat i do docker containeru, ale indeed nefunguje v dockeru protože 
vyžaduje headless nastavení chromu, a to je pak automaticky detekováno cz.indeed.com a pošle tě s tim někam.

údaje které jsou scrapovany jsou pozice, popis, místo a firma, případně plat pokud je k dispozici.

snad to někomu pomůže, sám jsem zkoušel scrapery hledat, a na githubu jich moc není, nebou jsou outdated. ChatGPT taky moc nepomohlo, takže tak.

pozn: chromedriver je automaticky nainstalovanej skrze chromedriver_autoinstall package takže ho nemusíte řešit
