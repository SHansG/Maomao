const dbName = process.env.APP_DB;
const appUser = process.env.APP_USER;
const appPass = process.env.APP_PASS;

const appDb = db.getSiblingDB(dbName);
const existing = appDb.getUser(appUser);

if (existing) {
  appDb.updateUser(appUser, {
    pwd: appPass,
    roles: [{ role: "readWrite", db: dbName }]
  });
  print(`Updated user ${appUser} on ${dbName}`);
} else {
  appDb.createUser({
    user: appUser,
    pwd: appPass,
    roles: [{ role: "readWrite", db: dbName }]
  });
  print(`Created user ${appUser} on ${dbName}`);
}
