function nomalize(v: number): string {
  if (v < 10) {
    return `0${v}`
  }
  return `${v}`
}

export function isRecentDate(date: Date, now: Date): boolean {
  const dayInMilliSeconds = 86400000;
  const nowStamp = now.getTime();
  const dateStamp = date.getTime();
  return nowStamp - dateStamp <= dayInMilliSeconds;
}

export function dateToPresentationString(date: Date, now: Date): string {
  if (isRecentDate(date, now)) {
    const hour = date.getHours();
    const minute = date.getMinutes();
    if (hour >= 12) {
      return `오후 ${nomalize(hour - 12)}:${nomalize(minute)}`
    }
    return `오전 ${nomalize(hour)}:${nomalize(minute)}`
  }

  return date.toDateString();
}
