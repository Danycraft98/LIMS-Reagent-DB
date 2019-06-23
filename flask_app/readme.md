from flask_app import db

db.create_all()
db.session.add(___)
db.session.commit()

User.query.get(_ )
User.query.all()
User.query.first()
User.query.filter_by(___).all()
User.query.filter_by(___).first()

table = Table(title="table1")
data1 = Data(POCP=2, AGILE=2, OCT=2, IDH=2, table_id=table.id)




	<!--article class="media content-section">
		<div class="media-body">
			<div class="article-metadata">
				<a class="mr-2" href="#">{{ post.author }}</a>
				<small class="text-muted">{{ post.date_posted }}</small>
			</div>
			<h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
			<p class="article-content">{{ post.content }}</p>
		</div>
      </article-->