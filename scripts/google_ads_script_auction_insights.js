/**
 * 好享宅家床墊 — 競價分析快照（舊版 AWQL 報表）
 * 設定排程：週一 10:50、週五 10:50（台北時間）
 */

var SHEET_ID = "1QOmQ9ziZD_mlJXOFk45oViq22vQfwXYl4GqGgMcYb7Q";
var SHEET_NAME = "競價分析_快照";

function main() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);

  var today = new Date();
  var dayOfWeek = today.getDay();
  var runType = dayOfWeek === 1 ? "週一" : dayOfWeek === 5 ? "週五" : "手動";
  var taipeiDate = Utilities.formatDate(today, "Asia/Taipei", "yyyy-MM-dd HH:mm");

  // 舊版 AWQL 競價分析報表
  var report = AdsApp.report(
    "SELECT Domain, ImpressionShare, OverlapRate, OutrankingShare, " +
    "PositionAboveRate, TopOfPageRate, AbsoluteTopOfPageRate " +
    "FROM AUCTION_INSIGHT_PERFORMANCE_REPORT " +
    "DURING LAST_7_DAYS"
  );

  var rows = report.rows();
  var newRows = [];

  while (rows.hasNext()) {
    var row = rows.next();
    newRows.push([
      taipeiDate,
      runType,
      row["Domain"],
      parseFloat(row["ImpressionShare"]) || 0,
      parseFloat(row["TopOfPageRate"]) || 0,
      parseFloat(row["AbsoluteTopOfPageRate"]) || 0,
      parseFloat(row["OverlapRate"]) || 0,
      parseFloat(row["OutrankingShare"]) || 0,
      parseFloat(row["PositionAboveRate"]) || 0
    ]);
  }

  if (newRows.length > 0) {
    sheet.getRange(sheet.getLastRow() + 1, 1, newRows.length, 9).setValues(newRows);
    Logger.log("✅ 寫入 " + newRows.length + " 筆競品資料 [" + runType + " " + taipeiDate + "]");
  } else {
    Logger.log("⚠️ 未取得資料");
  }
}
