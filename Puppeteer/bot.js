const puppeteer = require('puppeteer');
//const iPhone = puppeteer.devices['iPhone 6'];

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  //await page.emulate(iPhone);
  await page.goto('https://www.netmeds.com/customer/account/login');

  const [txt_Mobile_No] = await page.$x('//*[@id="loginfirst_mobileno"]');
  await txt_Mobile_No.type('<MobileNo>');
  const [button] = await page.$x(
    '/html/body/app-root/app-layout/div/main/app-login/div[1]/div/div[1]/div[2]/div/div[1]/form/div[2]/button[2]'
  );

  await button.click();
  await page.waitForXPath('//*[@id="login_received_pwd"]');
  const [pwd] = await page.$x('//*[@id="login_received_pwd"]');
  await pwd.type('<pwd>');
  const [submit] = await page.$x(
    '/html/body/app-root/app-layout/div/main/app-login/div[1]/div/div/div[2]/div[1]/form/div[2]/div[1]/button'
  );
  await submit.click();
  await page.waitForXPath('/html/body/div[1]/header/div/div/div[3]/a');
  const [upload_prescription_link] = await page.$x(
    '/html/body/div[1]/header/div/div/div[3]/a'
  );
  await upload_prescription_link.click();
  await page.waitForXPath(
    '/html/body/app-root/app-layout/div/main/app-m2/div[1]/div/div[1]/div[1]/div[2]/div/form/div[1]/ul/li[1]/label/input'
  );

  // File Upload Logic
  const [FileChooser] = await Promise.all([
    page.waitForFileChooser(),
    page.click('.up-fileupload'),
  ]);
  await FileChooser.accept(['prescription.jpg']);
  await page.waitForTimeout(1000);
  await page.click('.action-col');

  console.log('order confirmed');
  await page.waitForTimeout(10000);
  const [order_confirm] = await page.$x(
    '//*[@id="app"]/main/app-m2review/div[1]/div/div[2]/div/div[1]/div[3]/div[2]/button'
  );
  await order_confirm.click();

  await page.waitForTimeout(6000);
  //Take OrderConfirmation ScreenShot
  await page.screenshot({ path: 'order.jpg' });
  await page.waitForTimeout(6000);
  await browser.close();
})();
