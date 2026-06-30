fetch("data.json")
  .then(res => res.json())
  .then(data => {
    renderChart(data);
  });

function renderChart(data) {
  // group by date + source, compute average sentiment
  const grouped = {};

  data.forEach(row => {
    const key = row.date + "|" + row.source;
    if (!grouped[key]) grouped[key] = { sum: 0, count: 0 };
    grouped[key].sum += row.sentiment;
    grouped[key].count += 1;
  });

  // organize into { source: { date: avgSentiment } }
  const sources = {};
  for (const key in grouped) {
    const [date, source] = key.split("|");
    if (!sources[source]) sources[source] = {};
    sources[source][date] = grouped[key].sum / grouped[key].count;
  }

  // get all unique dates, sorted
  const allDates = [...new Set(data.map(d => d.date))].sort();

  // build a dataset per source
  const colors = { "BBC": "#1f77b4", "Al Jazeera": "#ff7f0e", "NYT": "#2ca02c" };
  const datasets = Object.keys(sources).map(source => ({
    label: source,
    data: allDates.map(date => sources[source][date] ?? null),
    borderColor: colors[source] || "#888",
    fill: false,
    tension: 0.2
  }));

  new Chart(document.getElementById("sentimentChart"), {
    type: "line",
    data: {
      labels: allDates,
      datasets: datasets
    },
    options: {
      scales: {
        y: {
          min: -1,
          max: 1,
          title: { display: true, text: "Avg Sentiment" }
        }
      }
    }
  });
}