<h2>Quick Explanation</h2>
<ul>
  <li>Import workflows: "Duo - Authorize" (child) and "Duo - Authorization Frontend Example" (parent)</li>
  <li>On the parent workflow, edit the "setUsername" MemorySet activity with the Duo username to which the authorization request will be sent.</li>
  <li>On the parent workflow, ensure that the "sendDuoAuth" RunWorkFlow activity is correctly pointing to the "Duo - Authorize" workflow.</li>
  <li>On the child workflow, your Duo API's specific endpoint URL, as well as integration key and secret key, must be set in the first three MemorySet activities ("setAPI", "setIntegrationKey", "setSecretKey").
  <li>Execute the parent workflow and watch as the "duoAuthResponse" DisplayValue activity displays either "allow" or "deny" based on the response received by the Duo user upon receiving their authorization request.</li>
</ul>

<b>Detailed Tutorial PDF:</b> <a href="https://github.com/Ayehu/custom-workflows/raw/master/Duo/Tutorial%20-%20Integrating%20with%20Duo%20for%20MFA%20(multi-factor%20authentication).pdf">https://github.com/Ayehu/custom-workflows/raw/master/Duo/Tutorial%20-%20Integrating%20with%20Duo%20for%20MFA%20(multi-factor%20authentication).pdf</a>

<b>Detailed Tutorial Support Article:</b> <a href="https://support.ayehu.com/hc/en-us/articles/360042165574">https://support.ayehu.com/hc/en-us/articles/360042165574</a>
