> pygame - 스타포스 강화 게임
>   
>

<br>
pymongo를 이용하여 mongoDB 와 연동하여 로그인을 할 수 있으며 회원가입은 존재하지 않는다

대신 존재하지 않는 ID와 패스워드 입력 시 입력한 ID와 패스워드로 **자동으로 회원가입**된다

물론 **이미 존재하는 ID로 로그인** 하는 경우에는 패스워드가 틀리면 **로그인에 실패**하게 된다

ID와 패스워드의 **포커스 전환**은 TAB키, 그리고 **로그인**은 ENTER키 입력으로 동작한다

해당 내용는 우측 상단의 **F1 도움말**에서도 확인할 수 있다
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/FWvSp/btrACMzY8jr/4TimyPYFtTtBWiA7OYg4uK/img.png"></p>
<br>
로그인을 하게 되면 **현재 랭킹을 조회**할 수 있고 화면에 표시된 랭킹은 **강화를 할 때 마다 갱신**된다

DB에서 **로그인한 ID의 현재 강화수치**를 불러오고, 화면에는 다음 단계 강화에 대한 **확률**이 표시된다

**스타캐치 해제**를 체크하면 스타캐치 없이 강화가 진행되며, 체크하지 않으면 **스타캐치 화면**으로 이동한다
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/btn2pn/btrAFNKXlDq/acn8QVY0j7Q7LDsJPHFTik/img.png"></p>
<br>
로그인 이후 F1 도움말키를 누르면 현재까지 강화를 몇번 시도했는지 **총 강화횟수**를 확인할 수 있다
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/cfDp3R/btrAAce4f5x/SKGH96CKkjept0p1uWDVLk/img.png"></p>
<br>
별이 가운데 노란영역 안에 있을때 **STOP 버튼을 클릭하거나 스페이스바 키를 입력**하면 

CATCH 텍스트가 나오면서 **강화 확률이 소폭 상승**한다

실패 시 **스타캐치 해제한 확률과 동일한 확률**로 강화가 진행된다
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/ciC9mI/btrABJXsVSA/DlQXqQPp8Kxq47Ziq6xlQ1/img.png"></p>
<br>
강화 수치 12성 이후부터는 **장비 파괴** 확률이 존재한다

장비가 파괴 될 경우 강화수치는 **0으로 초기화**된다
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/bn1eQp/btrADTrSMk3/vJzDw1z5kqPgkFGCzKzkdk/img.png"></p>
<br>

**사용자의 데이터는 다음과 같이 DB에 저장된다**
<br>
<p align="center"><img src="https://blog.kakaocdn.net/dn/8daqN/btrAFNKYJGl/QV3gsk48x23acgjpd1CmS0/img.png"></p>
<br>
<p align="center" style="text-align: center;" data-ke-size="size16"><a title="게임 다운로드" href="https://files.slack.com/files-pri/T039CS8AH0D-F03CYR3ECDQ/download/starforce_0.2.1.zip?origin_team=T039CS8AH0D" target="_blank" rel="noopener">게임 다운로드</a></p>
<p data-ke-size="size16">&nbsp;</p>
