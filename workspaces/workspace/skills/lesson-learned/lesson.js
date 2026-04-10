#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const LESSON_DIR = path.join(__dirname, '..', '..', 'lessons');
const MEMORY_FILE = path.join(__dirname, '..', '..', 'MEMORY.md');

function fmtDate() {
  return new Date().toISOString().slice(0, 10);
}
function fmtTime() {
  return new Date().toLocaleTimeString('en-GB', { hour12: false });
}

function ensureDir() {
  if (!fs.existsSync(LESSON_DIR)) fs.mkdirSync(LESSON_DIR, { recursive: true });
}

function todayFile() {
  return path.join(LESSON_DIR, `${fmtDate()}.md`);
}

function logLesson({ category, lesson, error, improvement }) {
  ensureDir();
  const file = todayFile();
  const ts = fmtTime();
  const line = `| ${ts} | ${category} | ${lesson} | ${error || ''} | ${improvement || ''} |\n`;
  const header = `## Daily Lessons & Self-Improvement Log\n\n| Time | Category | Lesson Learned | Error / Root Cause | Improvement Action |\n|------|----------|----------------|--------------------|---------------------|\n`;
  if (!fs.existsSync(file)) fs.writeFileSync(file, header);
  fs.appendFileSync(file, line);
  console.log(`✅ Lesson logged: ${category} — ${lesson}`);
}

function dailySummary() {
  const file = todayFile();
  if (!fs.existsSync(file)) return console.log('No lessons logged today.');
  const content = fs.readFileSync(file, 'utf8');
  const matches = content.match(/\| \d{2}:\d{2} \| .* \|/g);
  console.log(`📊 Today’s lessons so far: ${matches ? matches.length : 0}`);
}

function migrateToMemory() {
  const files = fs.readdirSync(LESSON_DIR).filter(f => f.endsWith('.md')).sort();
  if (!files.length) return;
  const latest = files.pop();
  const content = fs.readFileSync(path.join(LESSON_DIR, latest), 'utf8');
  const lessons = content.split('\n').filter(l => l.match(/^\| \d{2}:\d{2}/));
  if (!lessons.length) return;
  const distilled = lessons.map(l => { const parts = l.split('|').slice(1, -1).map(p => p.trim()); return parts[2]; }).join('; ');
  const memory = fs.readFileSync(MEMORY_FILE, 'utf8');
  if (memory.includes('## Latest Lessons')) {
    const updated = memory.replace(/## Latest Lessons[\s\S]*?(?=\n##|\n$|$)/, `## Latest Lessons\n\n${distilled}\n`);
    fs.writeFileSync(MEMORY_FILE, updated);
  } else {
    fs.appendFileSync(MEMORY_FILE, `\n## Latest Lessons\n\n${distilled}\n`);
  }
  console.log('🔄 Migrated today’s lessons to MEMORY.md');
}

if (require.main === module) {
  const cmd = process.argv[2];
  if (cmd === 'log') {
    const [, , , category, lesson, error, improvement] = process.argv;
    logLesson({ category, lesson, error, improvement });
  } else if (cmd === 'summary') {
    dailySummary();
  } else if (cmd === 'migrate') {
    migrateToMemory();
  } else {
    console.log('Usage: node lesson.js log <category> <lesson> [error] [improvement]');
    console.log('       node lesson.js summary');
    console.log('       node lesson.js migrate');
  }
}

module.exports = { logLesson, dailySummary, migrateToMemory };